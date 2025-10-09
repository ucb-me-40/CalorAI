import json
import os
from pathlib import Path

# --- Configuration ---
# Assuming the script runs from /CalorAI/scripts/
# We use pathlib for robust cross-OS path handling.

# Resolve the absolute path of the script's directory (CalorAI/scripts/)
SCRIPT_DIR = Path(__file__).resolve().parent

# Input: /CalorAI/data/book/cengel_*_toc.json
TOC_FILE_PATH = SCRIPT_DIR.parent / 'data' / 'book' / 'cengel_9th_toc.json'

# Output: /CalorAI/data/rag_corpus.txt
RAG_CORPUS_PATH = SCRIPT_DIR.parent / 'data' / 'rag_corpus.txt'

def create_toc_rag_chunks():
    """
    Reads the cengel_*_toc.json, formats chapter/section data into RAG chunks,
    and appends them to the rag_corpus.txt.
    """
    print(f"Loading Table of Contents from: {TOC_FILE_PATH}")
    
    try:
        # Load the JSON data
        with open(TOC_FILE_PATH, 'r', encoding='utf-8') as f:
            toc_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at {TOC_FILE_PATH}. Aborting.")
        return
    except json.JSONDecodeError as e:
        # Enhanced error handling to print the specific JSON decoding issue.
        print(f"Error: Could not decode JSON from {TOC_FILE_PATH}.")
        print(f"JSON integrity check failed. Details: {e}")
        return

    # Extract general book metadata
    book_title = toc_data.get('title', 'Thermodynamics Textbook')
    book_authors = toc_data.get('authors', 'Unknown Authors')
    chapters = toc_data.get('chapters', [])
    
    if not chapters:
        print("Warning: No chapters found in the table of contents data. Nothing to process.")
        return

    rag_chunks = []
    
    # Create a general header for the book reference
    rag_chunks.append(
        f"### TEXTBOOK REFERENCE: {book_title}\n"
        f"**Authors:** {book_authors}\n\n"
        f"This section indexes all chapter titles and section headings for the book '{book_title}'.\n"
        f"---"
    )

    # Iterate through chapters and format the RAG chunk for each one
    for chapter in chapters:
        chapter_number = chapter.get('chapter_number', 'N/A')
        chapter_title = chapter.get('title', 'Untitled Chapter')
        sections = chapter.get('sections', [])
        
        # Start the chunk for the specific chapter
        chunk = (
            f"\n\n### CHAPTER {chapter_number}: {chapter_title}\n"
            f"**Source:** {book_title}\n\n"
            f"#### Sections Included:\n"
        )
        
        # Add sections as a bulleted list
        if sections:
            section_list = "\n".join([f"- {section}" for section in sections])
            chunk += section_list
        else:
            chunk += "- No detailed sections listed for this chapter."
            
        chunk += "\n---"
        rag_chunks.append(chunk)

    # --- Append to RAG Corpus File ---
    try:
        # Open in append mode ('a')
        with open(RAG_CORPUS_PATH, 'a', encoding='utf-8') as f:
            # Add two leading newlines to ensure separation from previous content
            f.write("\n\n")
            f.write("\n".join(rag_chunks))
        
        print(f"\nSuccessfully appended {len(chapters)} chapter chunks to {RAG_CORPUS_PATH}.")
        print(f"First chapter chunk created: \n{rag_chunks[1].strip()}")
        
    except Exception as e:
        print(f"\nError writing to RAG corpus file: {RAG_CORPUS_PATH}. Error: {e}")


if __name__ == '__main__':
    create_toc_rag_chunks()
