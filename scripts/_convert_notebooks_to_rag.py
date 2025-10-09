import json
import re
from pathlib import Path

# --- Configuration ---
# Assuming the script runs from /CalorAI/scripts/
SCRIPT_DIR = Path(__file__).resolve().parent

# Input: Directory where your Jupyter Notebooks (.ipynb) are stored
NOTEBOOKS_DIR = SCRIPT_DIR.parent / 'data' / 'examples' / 'jupyterNotebooks'

# Output: /CalorAI/data/rag_corpus.txt
RAG_CORPUS_PATH = SCRIPT_DIR.parent / 'data' / 'rag_corpus.txt'


def extract_metadata(notebook_path: Path) -> dict:
    """
    Parses the first cell of a Jupyter Notebook to extract the structured metadata.
    Includes robust fallbacks for common JSON syntax errors (single quotes, missing values, trailing commas).
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
            
        first_cell_source = "".join(notebook_data['cells'][0]['source'])
        
        # Use regex to find the JSON block enclosed by ```json ... ```
        match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", first_cell_source)
        
        if match:
            metadata_string_raw = match.group(1)
            
            # 1. Primary Cleanup: Convert notebook JSON internal escape sequences 
            # (escaped newlines and double quotes) into valid JSON format.
            # This is crucial for handling how jupyter stores markdown/code lines as an array of strings.
            metadata_string = metadata_string_raw.replace('\\n', '\n').replace('\\"', '"').strip()
            
            # --- ROBUSTNESS FIXES ---
            
            # 2. Fix missing values: Finds "key": , and replaces it with "key": null, 
            # This fixes malformed JSON where properties were left blank (e.g., "chapter_number": ,)
            metadata_string = re.sub(r'(".*?"\s*:\s*),\s*', r'\1null,', metadata_string)
            
            # 3. Fix trailing commas: Remove commas that appear right before a closing brace or bracket.
            # This is another common JSON parsing error source, especially in multi-line formats.
            metadata_string = re.sub(r',\s*([}\]])', r'\1', metadata_string, flags=re.MULTILINE)
            
            # --------------------------

            try:
                # FIRST ATTEMPT: Strict JSON load
                return json.loads(metadata_string)
            except json.JSONDecodeError as e:
                # SECOND ATTEMPT (Fallback): Handle common syntax errors (e.g., using single quotes instead of double quotes)
                if "Expecting property name enclosed in double quotes" in str(e):
                    # Replace single quotes with double quotes as a heuristic fix
                    metadata_string_fixed = metadata_string.replace("'", '"')
                    try:
                        # FINAL ATTEMPT with all fixes applied
                        return json.loads(metadata_string_fixed)
                    except json.JSONDecodeError as second_e:
                        print(f"Error extracting metadata from {notebook_path.name}: Failed to parse JSON even after fixing quotes, missing values, and trailing commas. Original Error: {e}")
                        return {}
                
                # Handle other decode errors (e.g., unexpected character, non-quoted string)
                print(f"Error extracting metadata from {notebook_path.name}: JSONDecodeError: {e}")
                return {}

        
        print(f"Warning: No metadata block found in {notebook_path.name}")
        return {}
    
    except Exception as e:
        print(f"Error extracting metadata from {notebook_path.name}: {e}")
        return {}


def convert_notebook_to_rag_chunk(notebook_path: Path, metadata: dict) -> str:
    """
    Converts a single Jupyter Notebook into a formatted RAG chunk string.
    
    *** UPDATED: Now includes lecture_id and subtopic keys in the output chunk. ***
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
    except Exception as e:
        return f"Error loading notebook file {notebook_path.name}: {e}"

    
    problem_title = metadata.get('problem_title', notebook_path.stem)
    topic = metadata.get('topic', 'N/A')
    
    # --- Reference Extraction with KEYS ---
    lecture_reference = metadata.get('lecture_reference', {})
    book_ref = metadata.get('book_reference', {})
    
    # Extract Subtopics, including the key
    subtopics = lecture_reference.get('subtopics', [])
    lecture_details = [
        f"Key: {s.get('key', 'N/A')} ({s.get('title', 'N/A')})" 
        for s in subtopics if s and (s.get('key') or s.get('title'))
    ]

    # Include the main Lecture ID
    lecture_id = lecture_reference.get('lecture_id')
    if lecture_id:
        lecture_details.insert(0, f"Lecture ID: {lecture_id}")

    # Safely handle null/None values from cleaned JSON
    book_details_chapter = book_ref.get('chapter_number') or '?'
    book_details_title = book_ref.get('title') or 'N/A'
        
    book_details = f"Book Ch. {book_details_chapter}: {book_details_title}"
    
    # --- Content Aggregation ---
    markdown_chunks = []
    code_chunks = []
    
    # Start iterating from the second cell (index 1) to skip the metadata cell
    for cell in notebook_data['cells'][1:]:
        source = "".join(cell['source']).strip()
        if not source:
            continue
            
        if cell['cell_type'] == 'markdown':
            markdown_chunks.append(source)
        elif cell['cell_type'] == 'code':
            # Code blocks are wrapped for clear visualization in the corpus
            code_chunks.append(f"```python\n{source}\n```")


    # --- Construct the final RAG Chunk ---
    chunk = [
        f"### PROBLEM: {problem_title}",
        f"**Source:** Jupyter Notebook ({notebook_path.name})",
        f"**Topic:** {topic}",
        f"**Lecture References:** {', '.join(lecture_details)}", # Updated line
        f"**Book Reference:** {book_details}",
        "\n#### Discussion / Problem Statement:",
        # Use only the first few markdown cells for the main discussion
        "\n".join(markdown_chunks[:3]), 
        "\n#### Solution Code:",
        # All code goes here
        "\n".join(code_chunks),
        "\n#### Final Summary / Reasoning:",
        # Find the last piece of markdown which is often the summary/reasoning (like in your example)
        "\n".join(markdown_chunks[-2:]),
        "\n---" # Hard separator for RAG
    ]
    
    return "\n".join(chunk)


def append_notebooks_to_corpus():
    """
    Finds all Jupyter notebooks in the NOTEBOOKS_DIR and appends their content 
    as RAG chunks to the rag_corpus.txt file.
    """
    
    # Note: glob() only finds files directly in the directory.
    # If your files are deeper, you might need to use recursive=True.
    notebook_files = list(NOTEBOOKS_DIR.glob('*.ipynb'))
    
    if not notebook_files:
        print(f"No Jupyter notebooks found in {NOTEBOOKS_DIR}. Skipping RAG update.")
        
        # Check if the directory exists
        if not NOTEBOOKS_DIR.is_dir():
            print(f"ACTION REQUIRED: The directory {NOTEBOOKS_DIR} does not exist.")
            print("Please create this directory and move your .ipynb files there.")
            
        return

    print(f"Found {len(notebook_files)} notebooks to process.")
    processed_count = 0
    
    # We open the corpus file in append mode ('a')
    with open(RAG_CORPUS_PATH, 'a', encoding='utf-8') as corpus_file:
        for nb_path in notebook_files:
            metadata = extract_metadata(nb_path)
            if not metadata:
                continue
                
            chunk = convert_notebook_to_rag_chunk(nb_path, metadata)
            
            # Ensure the chunk starts with a newline if the file didn't end with one
            if not chunk.startswith('\n'):
                corpus_file.write("\n")
                
            corpus_file.write(chunk)
            processed_count += 1
            
            # Use metadata.get safely as it might be {} if parsing failed but was allowed to continue
            print(f"-> Successfully appended: {metadata.get('problem_title', nb_path.stem)}")

    print(f"\nCompleted appending {processed_count} notebook examples to {RAG_CORPUS_PATH.name}.")
    
    
if __name__ == '__main__':
    # NOTE: Ensure your Jupyter Notebooks are located in the following path:
    # /CalorAI/examples/jupyterNotebooks/
    append_notebooks_to_corpus()
