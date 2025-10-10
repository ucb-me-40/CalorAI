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
    # re.DOTALL makes '.' match newlines
    cleaned_text = re.sub(pattern, cleaner, text, flags=re.DOTALL)
    
    return cleaned_text

# --- File Processing ---

# Define paths relative to the project root /CalorAI
# The script assumes it is executed from /CalorAI
data_dir = Path('data')
input_file_path = data_dir / 'rag_corpus.txt'
output_file_path = data_dir / 'rag_corpus_cleaned.txt' # Output goes into /CalorAI/data

try:
    # 1. Read the entire corpus file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        raw_corpus_text = f.read()

    # 2. Clean the formulas
    cleaned_corpus_text = clean_latex_formulas(raw_corpus_text)

    # 3. Write the cleaned content to the new file
    with open(output_file_path, 'w', encoding='utf-8') as f:
        f.write(cleaned_corpus_text)

    print(f"Successfully cleaned formulas and saved to: {output_file_path}")

except FileNotFoundError:
    print(f"Error: The file '{input_file_path}' was not found. Check if it exists in the 'data/' directory.")