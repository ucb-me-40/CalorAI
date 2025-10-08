import os
import json
import glob

# --- Configuration ---
# The script assumes it is executed from the '../me40-slm/python' directory.

# 1. Location of the JSON files to be merged:
# SCRIPT LOCATION: ../me40-slm/python
# JSON FILES LOCATION: ../me40-slm/examples/json
JSON_DIR_RELATIVE = '../examples/json'

# 2. Destination for the final merged JSON file:
# OUTPUT FOLDER LOCATION: ../me40-slm/jsonTrainingData/v1.1
OUTPUT_DIR_RELATIVE = '../jsonTrainingData/v1.1' 

# 3. Name of the final merged output file:
OUTPUT_FILENAME = 'examples.json'
# --- End Configuration ---

def merge_json_files(json_dir, output_dir, output_filename):
    """
    Finds all JSON files in the specified directory and merges their contents
    into a single list (JSON array) in the specified output file path.
    """
    
    # 1. Define paths and ensure output directory exists
    search_path = os.path.join(json_dir, '*.json')
    json_files = glob.glob(search_path)
    output_full_path = os.path.join(output_dir, output_filename)
    
    if not json_files:
        print(f"No JSON files found in '{json_dir}'. Please check the directory path.")
        return

    # Create the output directory if it does not exist
    os.makedirs(output_dir, exist_ok=True)
    print(f"Found {len(json_files)} JSON files to merge.")

    merged_data = []
    
    # 2. Read and merge data
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Merge logic: assumes contents can be combined into a single master list
                if isinstance(data, list):
                    merged_data.extend(data)
                else:
                    merged_data.append(data)
                    
                print(f"  Successfully processed: {file_path}")
                
        except json.JSONDecodeError as e:
            print(f"ERROR: Could not decode JSON in file {file_path}. Skipping.")
            print(f"  Details: {e}")
        except Exception as e:
            print(f"ERROR: An unexpected error occurred while processing {file_path}. Skipping.")
            print(f"  Details: {e}")

    # 3. Write the merged data to the output file
    try:
        with open(output_full_path, 'w', encoding='utf-8') as f:
            # Use indent=4 for a human-readable, formatted output
            json.dump(merged_data, f, indent=4)
            
        print(f"\n✅ Merge complete! The final file has been created at:")
        print(f"   '{output_full_path}'")
        print(f"It contains {len(merged_data)} records in a single JSON array.")
    except Exception as e:
        print(f"ERROR: Could not write to output file '{output_full_path}': {e}")

# Execute the merge function
if __name__ == "__main__":
    merge_json_files(JSON_DIR_RELATIVE, OUTPUT_DIR_RELATIVE, OUTPUT_FILENAME)