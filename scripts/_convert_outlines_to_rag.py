import json
from pathlib import Path
import re 
from json.decoder import JSONDecodeError # Import the specific error type

# --- Configuration ---
# Assuming the script runs from /CalorAI/scripts/
SCRIPT_DIR = Path(__file__).resolve().parent

# Input: Base directory where lecture outlines are stored
# This will search recursively for all 'outline.json' files within this path.
OUTLINES_BASE_DIR = SCRIPT_DIR.parent / 'data' / 'courseInstances' / 'Fa25'

# Output: /CalorAI/data/rag_corpus.txt
RAG_CORPUS_PATH = SCRIPT_DIR.parent / 'data' / 'rag_corpus.txt'
# --- End Configuration ---


def format_subtopic_chunk(lecture_title: str, subtopic: dict) -> str:
    """
    Formats an individual subtopic object into a clean RAG chunk.
    This chunk is designed to provide context for the specific video segment.
    """
    # Use the lecture title as the overarching context
    source_title = f"{lecture_title} (Outline)"
    
    # Extract key information, falling back to 'N/A' if missing
    key = subtopic.get('key', 'N/A')
    title = subtopic.get('title', 'N/A')
    time_range = subtopic.get('time_range', 'N/A')
    summary = subtopic.get('detailed_summary') or subtopic.get('summary', 'No detailed summary provided.')
    
    # IMPORTANT FIX: Undo JSON escaping. Convert double backslashes (\\) back to
    # single backslashes (\) so LaTeX commands (like \eta) are correctly formatted
    # in the final RAG corpus text file.
    summary_clean = summary.strip().replace('\\\\', '\\')
    
    # Format the chunk
    chunk = [
        f"### LECTURE SUBTOPIC: {title}",
        f"**Source:** {source_title}",
        f"**Video Key:** {key} (Time: {time_range})",
        f"**Content Summary:**",
        summary_clean, # Use the cleaned summary
        "\n---" # Hard separator for RAG
    ]
    
    # Note: Using "\n" in the chunk list helps control line breaks more cleanly
    return "\n".join(chunk)

def append_outlines_to_corpus():
    """
    Finds all outline.json files recursively and appends their subtopic content
    as RAG chunks to the rag_corpus.txt file.
    
    This version applies structural fixes but *removes* the backslash escape
    to let the user manually fix 'Invalid \escape' errors using the precise 
    line/column reported.
    """
    
    # Find all 'outline.json' files recursively starting from the base directory
    outline_files = list(OUTLINES_BASE_DIR.glob('**/outline.json'))
    
    if not outline_files:
        print(f"No 'outline.json' files found in {OUTLINES_BASE_DIR}. Skipping outline processing.")
        return

    print(f"Found {len(outline_files)} lecture outline files to process.")
    processed_subtopics_count = 0
    
    # Open the corpus file in append mode ('a')
    with open(RAG_CORPUS_PATH, 'a', encoding='utf-8') as corpus_file:
        for outline_path in outline_files:
            try:
                # 1. Read the file content as a single raw string.
                raw_content = outline_path.read_text(encoding='utf-8')

                # --- STRUCTURAL JSON STRING CLEANUP (Keeping only syntax fixes) ---
                
                # 2. Fix missing values: Finds "key": , and replaces it with "key": null, 
                content_fixed_1 = re.sub(r'(".*?"\s*:\s*),\s*', r'\1null,', raw_content)

                # 3. Fix trailing commas: Remove commas that appear right before a closing brace or bracket.
                content_final = re.sub(r',\s*([}\]])', r'\1', content_fixed_1, flags=re.MULTILINE)
                
                # --- NOTE: Removed the global .replace('\\', '\\\\') to prevent 
                # --- over-escaping, specifically of '\"' characters.
                
                # 4. Parse the cleaned string
                outline_data = json.loads(content_final)
                    
            except JSONDecodeError as e:
                # Provide explicit line and column number for JSON syntax errors
                error_message = f"JSON Syntax Error in {outline_path} at **Line {e.lineno}, Column {e.colno}**. Error: {e.msg}"
                print(f"Error loading or parsing JSON from {outline_path}: {error_message}")
                continue
            except Exception as e:
                # Catch other potential errors (like file IO)
                print(f"General Error loading or parsing {outline_path}: {e}")
                continue

            # Extract top-level lecture details
            lecture_id = outline_data.get('lectureId', 'N/A')
            lecture_name = outline_data.get('title', outline_path.parent.name)
            
            # Get the list of subtopics
            subtopics = outline_data.get('subtopics', [])
            
            if not subtopics:
                print(f"Warning: No subtopics found in {outline_path.parent.name}/outline.json. Skipping.")
                continue

            print(f"-> Processing Lecture: {lecture_name} (ID: {lecture_id}) with {len(subtopics)} subtopics.")

            # Iterate through subtopics and create RAG chunks
            for subtopic in subtopics:
                chunk = format_subtopic_chunk(lecture_name, subtopic)
                
                # Write the chunk to the corpus file
                if not chunk.startswith('\n'):
                    corpus_file.write("\n")
                corpus_file.write(chunk)
                processed_subtopics_count += 1

    print(f"\nCompleted appending {processed_subtopics_count} subtopic entries to {RAG_CORPUS_PATH.name}.")
    
    
if __name__ == '__main__':
    append_outlines_to_corpus()
