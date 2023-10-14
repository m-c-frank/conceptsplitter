import os
import re
from interface import extract_atomic_concepts

# Constants
SOURCE_PATH = os.path.expanduser("~/Downloads")
RESULT_PATH = os.path.expanduser("~/some/other/path")

def get_text_files(directory):
    """Return a list of files that have the 'text-' prefix."""
    return [f for f in os.listdir(directory) if f.startswith("text-")]

def read_file(filepath):
    """Read and return content of a file."""
    with open(filepath, 'r') as file:
        return file.read()

def save_concepts(concepts, filename):
    """Save extracted concepts to a file."""
    title = "Extracted_From_" + filename
    result_path = os.path.join(RESULT_PATH, title)
    with open(result_path, 'w') as file:
        file.write(concepts)

def main():
    files = get_text_files(SOURCE_PATH)
    print(f"Found {len(files)} text files to process.")

    for filename in files:
        print(f"Processing: {filename}")
        content = read_file(os.path.join(SOURCE_PATH, filename))
        concepts = extract_atomic_concepts(content)
        save_concepts(concepts, filename)
        print(f"Saved extracted concepts from {filename}.")

if __name__ == "__main__":
    main()
