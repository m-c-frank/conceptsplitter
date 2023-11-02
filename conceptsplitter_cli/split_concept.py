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

logger = logging.getLogger(__name__)

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_documents(input_directory):
    logger.debug(f"Loading documents from directory: {input_directory}")
    return ObsidianLoader(path=input_directory).load()

def extract_single_concept(concept_title, source_context):
    concept_content, concept_tags = get_concept_content(concept_title, source_context)
    return {
        "title": concept_title,
        "content": concept_content,
        "tags": split_concept_tags(concept_tags),
    }

def extract_concepts_from_document(doc):
    logger.info(f"Extracting concepts from {doc}")
    extracted_concept_titles = split_concept_titles(get_concept_titles(doc.page_content))

    concepts = [extract_single_concept(title, doc.page_content) for title in extracted_concept_titles]
    linked_concept_content, linked_concept_tags = get_linked_concept_content(concepts, doc.page_content)

    concepts.append({
        "title": get_concept_title(linked_concept_content),
        "content": linked_concept_content,
        "tags": split_concept_tags(linked_concept_tags),
        "metadata": doc.metadata,
    })
    return concepts

def write_concept_to_file(concept, output_directory):
    concept_title = concept["title"]
    content = f"# {concept_title}\n\n{concept['content']}"
    note_filename = os.path.join(output_directory, f"{concept_title.replace(' ', '_')}.md")

    with open(note_filename, "w") as note_file:
        note_file.write(content)

def generate_notes(concepts, output_directory):
    ensure_directory_exists(output_directory)
    [write_concept_to_file(concept, output_directory) for concept in concepts]

def main(input_directory, output_directory):
    docs = load_documents(input_directory)
    all_concepts = [concept for doc in docs for concept in extract_concepts_from_document(doc)]

    logger.info(f"Extracted {len(all_concepts)} concepts")
    generate_notes(all_concepts, output_directory)
