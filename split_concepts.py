import os
import argparse
from langchain.document_loaders import ObsidianLoader
from interface import (
    get_concept_titles,
    get_concept_content,
    get_linked_concept_content,
    get_concept_title,
)


def ensure_directory_exists(directory):
    """Ensure the directory exists. If not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def extract_concepts_from_directory(input_directory):
    """Extract concepts from the Obsidian markdown files in the provided directory."""
    loader = ObsidianLoader(path=input_directory)
    docs = loader.load()

    concepts = []
    for doc in docs:
        extracted_concept_titles = get_concept_titles(doc.page_content)
        for concept_title in extracted_concept_titles:
            result = get_concept_content(
                concept_title=concept_title, source_context=doc.page_content
            )
            concept_content, concept_tags = result

            concepts.append(
                {
                    "title": concept_title,
                    "content": concept_content,
                    "tags": concept_tags,
                }
            )

        result = get_linked_concept_content(
            concepts=concepts, source_context=doc.page_content
        )

        concept_content, concept_tags = result

        concepts.append(
            {
                "title": get_concept_title(concept_content),
                "content": concept_content,
                "tags": concept_tags,
                "metadata": doc.metadata,
            }
        )

    return concepts


def generate_notes(concepts, output_directory):
    """Generate individual notes for each extracted concept."""
    ensure_directory_exists(output_directory)

    for concept in concepts:
        concept_title = concept["title"]
        concept_content = concept["content"]
        note_content = f"# {concept_title}\n\n{concept_content}"
        note_filename = os.path.join(
            output_directory, f"{concept_title.replace(' ','_')}.md"
        )
        with open(note_filename, "w") as note_file:
            note_file.write(note_content)


def generate_link_file(concepts, output_directory):
    """Generate a file that describes how the concepts were linked in the original markdown files."""
    pass


def main():
    """Main function to handle command-line inputs and execute the concept extraction."""
    parser = argparse.ArgumentParser(description="Concept Extraction from Markdown")
    parser.add_argument(
        "input_directory", help="Path to the directory containing markdown files"
    )
    parser.add_argument(
        "--output",
        default="./output",
        help="Path to the output directory where the notes will be saved",
    )

    args = parser.parse_args()

    concepts = extract_concepts_from_directory(args.input_directory)

    generate_notes(concepts, args.output)
    generate_link_file(concepts, args.output)


if __name__ == "__main__":
    main()
