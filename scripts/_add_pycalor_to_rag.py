import os

def append_pycalor_docs_to_rag():
    """
    Extracts the documentation for the 'state' and 'process' classes from 
    README.md and appends it as a structured block to rag_corpus.txt.
    """
    
    # Define file paths
    README_FILE = "../../berkeley/me40/README.md"
    RAG_CORPUS_FILE = "data/rag_corpus.txt"
    
    # --- 1. Read README.md content ---
    try:
        with open(README_FILE, 'r') as f:
            readme_content = f.read()
    except FileNotFoundError:
        print(f"Error: The source file '{README_FILE}' was not found. Please ensure it is in the current directory.")
        return
    except Exception as e:
        print(f"Error reading {README_FILE}: {e}")
        return

    # --- 2. Define the start and end markers for the pyCalor documentation block ---
    # Start at the documentation for the 'state' class
    start_marker = "## Class **state**"
    # End just before the documentation for the 'hf_rec' class
    end_marker = "## Class hf_rec"

    start_index = readme_content.find(start_marker)
    
    if start_index == -1:
        print(f"Error: The documentation section '{start_marker}' was not found in {README_FILE}.")
        return

    # Search for the end marker starting from the documentation's beginning
    end_index = readme_content.find(end_marker, start_index) 

    if end_index == -1:
        # If the end marker is missing, take everything from the start marker to the end of the file
        pycalor_docs_raw = readme_content[start_index:].strip()
    else:
        # Otherwise, take the content between the markers
        pycalor_docs_raw = readme_content[start_index:end_index].strip()

    # --- 3. Format the content for the RAG corpus ---
    rag_block_header = "\n\n---\n## pyCalor Documentation (State and Process Classes)\n**Source:** pyCalor README.md\n"
    final_rag_entry = rag_block_header + pycalor_docs_raw + "\n"

    # --- 4. Append the content to rag_corpus.txt ---
    try:
        with open(RAG_CORPUS_FILE, 'a') as f:
            f.write(final_rag_entry)
            
        print(f"\n✅ Successfully added pyCalor documentation to '{RAG_CORPUS_FILE}'.")
        print("\nNEXT STEP: You must run '1_create_rag_index.py' to embed this new knowledge and make it available to CalorAI.")

    except Exception as e:
        print(f"Error writing to {RAG_CORPUS_FILE}: {e}")

if __name__ == "__main__":
    append_pycalor_docs_to_rag()
