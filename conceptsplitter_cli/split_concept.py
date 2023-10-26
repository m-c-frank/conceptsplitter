import os
import logging
from langchain.document_loaders import ObsidianLoader
from .interface import (
    get_concept_titles,
    get_concept_content,
    get_linked_concept_content,
    get_concept_title,
    split_concept_titles,
    split_concept_tags
)

# Get the logger for this module
logger = logging.getLogger(__name__)

def ensure_directory_exists(directory):
    """Ensure the directory exists. If not, create it."""
    if not os.path.exists(directory):
        os.makedirs(directory)


def load_documents_from_directory(input_directory):
    """Load documents from the input directory."""
    logger.debug(f"Loading documents from directory: {input_directory}")
    loader = ObsidianLoader(path=input_directory)
    return loader.load()


def extract_concepts_from_document(doc):
    """Extract concepts from a single Obsidian markdown document."""
    logger.info(f"Extracting concepts from {doc}")

    extracted_concept_titles = get_concept_titles(doc.page_content)
    extracted_concept_titles = split_concept_titles(extracted_concept_titles)

    logger.info(f"Extracted {len(extracted_concept_titles)} concepts: {extracted_concept_titles}")
    concepts = []

    for concept_title in extracted_concept_titles:
        logger.debug(f"Extracting concept {concept_title}")
        concept_content, concept_tags = get_concept_content(
            concept_title=concept_title, source_context=doc.page_content
        )
        concept_tags = split_concept_tags(concept_tags)
        logger.debug(f"Extracted concept content for {concept_title}: {concept_content}, Tags: {concept_tags}")

        concepts.append(
            {
                "title": concept_title,
                "content": concept_content,
                "tags": concept_tags,
            }
        )

    logger.debug("Extracting linked concepts")
    linked_concept_content, linked_concept_tags = get_linked_concept_content(
        concepts=concepts, source_context=doc.page_content
    )

    linked_concept_tags = split_concept_tags(linked_concept_tags)
    logger.debug(f"Linked concept content: {linked_concept_content}, Tags: {linked_concept_tags}")

    concepts.append(
        {
            "title": get_concept_title(linked_concept_content),
            "content": linked_concept_content,
            "tags": linked_concept_tags,
            "metadata": doc.metadata,
        }
    )

    return concepts


def generate_individual_note(concept, output_directory):
    """Generate an individual note for a single extracted concept."""
    concept_title = concept["title"]
    concept_content = concept["content"]
    note_content = f"# {concept_title}\n\n{concept_content}"
    note_filename = os.path.join(
        output_directory, f"{concept_title.replace(' ', '_')}.md"
    )

    with open(note_filename, "w") as note_file:
        note_file.write(note_content)


def generate_notes(concepts, output_directory):
    """Generate individual notes for each extracted concept."""
    ensure_directory_exists(output_directory)
    for concept in concepts:
        generate_individual_note(concept, output_directory)

def main(input_directory, output_directory):
    """Function to handle processing logic after arguments are parsed."""
    docs = load_documents_from_directory(input_directory)
    concepts = []

    for doc in docs:
        concepts.extend(extract_concepts_from_document(doc))

    logger = logging.getLogger(__name__)
    logger.info(f"Extracted {len(concepts)} concepts")
    generate_notes(concepts, output_directory)
