import re
from pathlib import Path

def clean_latex_formulas(text):
    """
    Removes all whitespace characters inside LaTeX double-dollar delimiters ($$).
    """
    # Pattern: \$\$ (start of block) + (.*?) (content) + \$\$ (end of block)
    pattern = r'\$\$(.*?)\$\$'

    def cleaner(match):
        # The content inside the $$ delimiters is group 1
        content = match.group(1)
        
        # Remove all whitespace characters (spaces, tabs, newlines)
        cleaned_content = re.sub(r'\s+', '', content)
        
        # Reconstruct the formula with the surrounding $$
        return f'$${cleaned_content}$$'

    # Use re.sub to apply the cleaner function to every match across the entire text
    # re.DOTALL makes '.' match newlines, which is crucial for multiline formulas
    cleaned_text = re.sub(pattern, cleaner, text, flags=re.DOTALL)
    
    return cleaned_text

# --- File Processing ---

# Define paths relative to the project root /CalorAI
data_dir = Path('data')
# *** MODIFICATION: Only one path is needed for both input and output ***
file_path = data_dir / 'rag_corpus.txt' 

try:
    # 1. Read the entire corpus file
    with open(file_path, 'r', encoding='utf-8') as f:
        raw_corpus_text = f.read()

    # 2. Clean the formulas
    cleaned_corpus_text = clean_latex_formulas(raw_corpus_text)

    # 3. Write the cleaned content to the original file path
    # 'w' (write) mode overwrites the entire file content.
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_corpus_text)

    print(f"✅ Successfully cleaned formulas and **overwrote** the original file: {file_path}")

except FileNotFoundError:
    print(f"❌ Error: The file '{file_path}' was not found. Check if it exists in the 'data/' directory.")