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
    (This function remains robust and targets the JSON block in Cell 0).
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
            
        if not notebook_data.get('cells') or len(notebook_data['cells']) == 0:
             return {}
             
        first_cell_source = "".join(notebook_data['cells'][0]['source'])
        
        # Use regex to find the JSON block enclosed by ```json ... ```
        match = re.search(r"```json\s*(\{[\s\S]*?\})\s*```", first_cell_source)
        
        if match:
            metadata_string_raw = match.group(1)
            
            # --- ROBUSTNESS FIXES ---
            metadata_string = metadata_string_raw.replace('\\n', '\n').replace('\\"', '"').strip()
            metadata_string = re.sub(r'(".*?"\s*:\s*),\s*', r'\1null,', metadata_string)
            metadata_string = re.sub(r',\s*([}\]])', r'\1', metadata_string, flags=re.MULTILINE)
            
            try:
                return json.loads(metadata_string)
            except json.JSONDecodeError as e:
                if "Expecting property name enclosed in double quotes" in str(e):
                    metadata_string_fixed = metadata_string.replace("'", '"')
                    try:
                        return json.loads(metadata_string_fixed)
                    except json.JSONDecodeError:
                        pass
                print(f"Error extracting metadata from {notebook_path.name}: JSONDecodeError: {e}")
                return {}

        return {}
    
    except Exception as e:
        print(f"Error extracting metadata from {notebook_path.name}: {e}")
        return {}


def convert_notebook_to_rag_chunk(notebook_path: Path, metadata: dict) -> str:
    """
    Converts a single Jupyter Notebook into a formatted RAG chunk string,
    adhering to the fixed cell structure.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook_data = json.load(f)
            cells = notebook_data.get('cells', [])
    except Exception as e:
        return f"Error loading notebook file {notebook_path.name}: {e}"
        
    if not cells:
        return ""

    
    problem_title = metadata.get('problem_title', notebook_path.stem)
    topic = metadata.get('topic', 'N/A')
    
    # --- RAG Header Data (Reference formatting logic is correct and unchanged) ---
    lecture_reference = metadata.get('lecture_reference', {})
    book_ref = metadata.get('book_reference', {})
    subtopics = lecture_reference.get('subtopics', [])
    lecture_details = [
        f"Key: {s.get('key', 'N/A')} ({s.get('title', 'N/A')})" 
        for s in subtopics if s and (s.get('key') or s.get('title'))
    ]
    lecture_id = lecture_reference.get('lecture_id')
    if lecture_id:
        lecture_details.insert(0, f"Lecture ID: {lecture_id}")

    book_details_chapter = book_ref.get('chapter_number') or '?'
    book_details_title = book_ref.get('title') or 'N/A'
    book_details = f"Book Ch. {book_details_chapter}: {book_details_title}"
    
    
    # --- 1. Problem Statement and Analysis (Fixed Indices 1, 2, 3, 4) ---
    problem_analysis_sources = []
    
    # Indices 1, 2, 3, and 4 (Problem, Schematic, Assumptions, Laws)
    for i in range(1, 5): 
        if len(cells) > i:
            cell = cells[i]
            source = "".join(cell['source']).strip()
            if source and cell.get('cell_type') == 'markdown':
                problem_analysis_sources.append(source)


    # --- 2. Final Summary / Reasoning (The Second-to-Last Cell: Index -2) ---
    summary_reasoning_src = ""
    # Check if the second-to-last cell exists (requires len > 1) and is markdown
    if len(cells) > 1 and cells[-2].get('cell_type') == 'markdown':
        summary_reasoning_src = "".join(cells[-2]['source']).strip()


    # --- 3. Solution Code (Cells from Index 5 up to Index -3, excluding the final two Markdown cells) ---
    code_chunks = []
    # Iterate from index 5 (first code cell) up to the second-to-last cell (index -2, the summary),
    # and excluding the last cell (index -1, the boilerplate). 
    # This means the slice ends at index -2.
    for cell in cells[5:-2]: 
        source = "".join(cell['source']).strip()
        
        # Only collect code blocks. 
        if source and cell.get('cell_type') == 'code':
            code_chunks.append(f"```python\n{source}\n```")


    # --- Construct the final RAG Chunk ---
    chunk = [
        f"### PROBLEM: {problem_title}",
        f"**Source:** Jupyter Notebook ({notebook_path.name})",
        f"**Topic:** {topic}",
        f"**Lecture References:** {', '.join(lecture_details)}", 
        f"**Book Reference:** {book_details}",
        
        "\n#### Problem Statement and Analysis:",
        # The mandatory discussion parts are joined here, with separators
        "\n\n---\n\n".join(problem_analysis_sources), 
        
        "\n#### Solution Code:",
        "\n".join(code_chunks),
        
        "\n#### Final Summary / Reasoning:",
        summary_reasoning_src, 
        
        "\n---" # Hard separator for RAG
    ]
    
    return "\n".join(chunk)


def append_notebooks_to_corpus():
    """
    Finds all Jupyter notebooks in the NOTEBOOKS_DIR and appends their content 
    as RAG chunks to the rag_corpus.txt file.
    """
    
    notebook_files = list(NOTEBOOKS_DIR.glob('*.ipynb'))
    
    if not notebook_files:
        print(f"No Jupyter notebooks found in {NOTEBOOKS_DIR}. Skipping RAG update.")
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
            
            if not chunk.startswith('\n'):
                corpus_file.write("\n")
                
            corpus_file.write(chunk)
            processed_count += 1
            
            print(f"-> Successfully appended: {metadata.get('problem_title', nb_path.stem)}")

    print(f"\nCompleted appending {processed_count} notebook examples to {RAG_CORPUS_PATH.name}.")
    
    
if __name__ == '__main__':
    append_notebooks_to_corpus()