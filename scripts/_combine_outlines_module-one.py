import json
import pathlib
import sys

# --- Configuration ---

# The base directory where the outlines are located.
# The script is assumed to be in 'python/' and the data is in '../courseInstances/'
BASE_DIR = pathlib.Path("../courseInstances")

# The name of the resulting combined JSON file.
OUTPUT_FILE = "../jsonTrainingData/v1.1/outline-module-one.json"

# List of relative directories where 'outline.json' is located.
# The script will look for BASE_DIR / path / 'outline.json'
RELATIVE_PATHS = [
    "Fa25/lecture-01a",
    "Fa25/lecture-01b",
    "Fa25/lecture-02a",
    "Fa25/lecture-02b",
    "Fa25/lecture-03a",
    "Fa25/lecture-03b",
    "Fa25/lecture-04a",
    "Fa23/lecture-04/specificHeat",
    "Fa23/lecture-04/specificHeatsIdealGases",
    "Fa25/lecture-04c",
    "Fa25/lecture-05a",
    "Fa25/lecture-05b",
    "Fa25/lecture-05c",
]

def combine_outlines():
    """Reads specified outline.json files and combines their content into a single JSON array."""
    combined_data = []
    print(f"Starting combination process from base directory: {BASE_DIR.resolve()}")
    print("-" * 30)

    for relative_path_str in RELATIVE_PATHS:
        # Construct the full path to the outline.json file
        full_path = BASE_DIR / relative_path_str / "outline.json"

        try:
            # 1. Check if the file exists
            if not full_path.exists():
                print(f"⚠️ File not found, skipping: {full_path}")
                continue

            print(f"✅ Reading: {full_path}")

            # 2. Read the file content and parse JSON
            with full_path.open('r', encoding='utf-8') as f:
                content = json.load(f)

            # 3. Add the content to the combined list.
            # Each file's content is wrapped in an object that includes the source path for context.
            combined_data.append({
                "source_path": str(full_path),
                "content": content
            })

        except json.JSONDecodeError as e:
            # This should ideally not happen now that the files are fixed, but keeps the original error reporting.
            print(f"❌ Error decoding JSON in {full_path}: {e}")
            print("   Content was skipped.")
        except Exception as e:
            print(f"Unhandled error processing {full_path}: {e}")

    # --- Write the final combined file ---
    if not combined_data:
        print("\nProcess finished, but no valid data was found to write.")
        return

    try:
        # Note: The output file will be written to the 'python/' directory where the script is run.
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out_f:
            # Dump the combined data, formatted with indentation for readability
            json.dump(combined_data, out_f, indent=4)

        print("\n" + "=" * 50)
        print(f"SUCCESS: Combined {len(combined_data)} outlines into {OUTPUT_FILE}")
        print(f"Output file saved to: {pathlib.Path(OUTPUT_FILE).resolve()}")
        print("=" * 50)

    except IOError as e:
        print(f"\nFATAL ERROR: Could not write to {OUTPUT_FILE}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    combine_outlines()
