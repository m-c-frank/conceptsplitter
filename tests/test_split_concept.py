import pytest
from conceptsplitter_cli import split_concept

def test_ensure_directory_exists_existing_directory(mocker):
    mocker.patch("os.path.exists", return_value=True)
    makedirs_mock = mocker.patch("os.makedirs")

    split_concept.ensure_directory_exists("test_directory")

    makedirs_mock.assert_not_called()

def test_ensure_directory_exists_non_existing_directory(mocker):
    mocker.patch("os.path.exists", return_value=False)
    makedirs_mock = mocker.patch("os.makedirs")

    split_concept.ensure_directory_exists("test_directory")

    makedirs_mock.assert_called_once_with("test_directory")

def test_load_documents_from_directory(mocker):
    mock_loader = mocker.MagicMock()
    mock_loader.load.return_value = ["doc1", "doc2"]
    mocker.patch("conceptsplitter_cli.split_concept.ObsidianLoader", return_value=mock_loader)

    docs = split_concept.load_documents_from_directory("test_directory")

    assert docs == ["doc1", "doc2"]

def test_extract_concepts_from_document(mocker):
    mocker.patch("conceptsplitter_cli.split_concept.get_concept_titles", return_value="ConceptTitle")
    mocker.patch("conceptsplitter_cli.split_concept.split_concept_titles", return_value=["Concept", "Title"])
    mocker.patch("conceptsplitter_cli.split_concept.get_concept_content", return_value=("ConceptContent", "ConceptTag"))
    mocker.patch("conceptsplitter_cli.split_concept.split_concept_tags", return_value=["Tag1", "Tag2"])

    doc_mock = mocker.MagicMock()
    doc_mock.page_content = "test_content"

    concepts = split_concept.extract_concepts_from_document(doc_mock)

    assert concepts[0]["title"] == "Concept"
    assert concepts[0]["content"] == "ConceptContent"
    assert concepts[0]["tags"] == ["Tag1", "Tag2"]

def test_generate_individual_note(mocker):
    concept = {
        "title": "ConceptTitle",
        "content": "ConceptContent"
    }
    output_directory = "test_directory"

    mocker.patch("os.path.join", return_value="test_directory/ConceptTitle.md")
    open_mock = mocker.mock_open()
    mocker.patch("builtins.open", open_mock)

    split_concept.generate_individual_note(concept, output_directory)

    open_mock.assert_called_once_with("test_directory/ConceptTitle.md", "w")

def test_generate_notes(mocker):
    concepts = [
        {"title": "Concept1", "content": "Content1"},
        {"title": "Concept2", "content": "Content2"}
    ]
    output_directory = "test_directory"

    ensure_dir_mock = mocker.patch("conceptsplitter_cli.split_concept.ensure_directory_exists")
    gen_note_mock = mocker.patch("conceptsplitter_cli.split_concept.generate_individual_note")

    split_concept.generate_notes(concepts, output_directory)

    ensure_dir_mock.assert_called_once_with(output_directory)
    assert gen_note_mock.call_count == 2

def test_main(mocker):
    input_directory = "input_dir"
    output_directory = "output_dir"

    load_docs_mock = mocker.patch("conceptsplitter_cli.split_concept.load_documents_from_directory", return_value=["doc1"])
    extract_concepts_mock = mocker.patch("conceptsplitter_cli.split_concept.extract_concepts_from_document", return_value=[{"title": "Concept", "content": "Content"}])
    generate_notes_mock = mocker.patch("conceptsplitter_cli.split_concept.generate_notes")

    split_concept.main(input_directory, output_directory)

    load_docs_mock.assert_called_once_with(input_directory)
    extract_concepts_mock.assert_called_once_with("doc1")
    generate_notes_mock.assert_called_once_with([{"title": "Concept", "content": "Content"}], output_directory)
