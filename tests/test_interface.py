import pytest
import json
from conceptsplitter_cli.interface import (
    split_concept_titles,
    split_concept_tags,
    get_concept_title,
    get_concept_titles,
    get_concept_content,
    get_linked_concept_content
)

# Helper function to mock the neural API
def mock_api(mocker, mock_data):
    mock_choice = {
        "message": {
            "function_call": {
                "arguments": json.dumps(mock_data)
            }
        }
    }
    mocker.patch('conceptsplitter_cli.interface.neuralapi.ChatCompletion.create', return_value=mocker.MagicMock(choices=[mock_choice]))

@pytest.mark.parametrize("input_data,expected", [
    ({'concept_titles': 'AI, Neural Networks, Deep Learning'}, ['AI', 'Neural Networks', 'Deep Learning']),
    ('AI, Neural Networks, Deep Learning', ['AI', 'Neural Networks', 'Deep Learning'])
])
def test_split_concepts(input_data, expected):
    # Arrange & Act
    if isinstance(input_data, dict):
        result = split_concept_titles(input_data)
    else:
        result = split_concept_tags(input_data)
    
    # Assert
    assert result == expected

def test_get_concept_title_with_valid_input(mocker):
    # Arrange
    mock_data = {"title": "AI Intro"}
    mock_api(mocker, mock_data)

    # Act
    result = get_concept_title('This is a text about AI.')

    # Assert
    assert result == 'AI Intro'

@pytest.mark.parametrize("input_text,mock_data,expected", [
    ('This is a text about AI.', {"concept_titles": "AI"}, ['AI']),
    ('This is a text about AI and Neural Networks.', {"concept_titles": "AI, Neural Networks"}, ['AI', 'Neural Networks'])
])
def test_get_concept_titles(mocker, input_text, mock_data, expected):
    # Arrange
    mock_api(mocker, mock_data)

    # Act
    result = get_concept_titles(input_text)
    result = split_concept_titles(result)

    # Assert
    assert result == expected

@pytest.mark.parametrize("concept,title_text,mock_data,expected_content,expected_tags", [
    ('AI', 'This is a text about AI.', {"concept_content": "AI is the simulation of human intelligence.", "concept_tags": "Simulation, Intelligence"}, 'AI is the simulation of human intelligence.', ['Simulation', 'Intelligence']),
    # You can expand this list with other test cases as needed
])
def test_get_concept_content(mocker, concept, title_text, mock_data, expected_content, expected_tags):
    # Arrange
    mock_api(mocker, mock_data)

    # Act
    content, tags = get_concept_content(concept, title_text)
    tags = split_concept_tags(tags)

    # Assert
    assert content == expected_content
    assert tags == expected_tags


@pytest.mark.parametrize("concepts,input_text,mock_data,expected_content,expected_tags", [
    ([
        {"title": "AI", "tags": ["Tech", "Intelligence"]},
        {"title": "Deep Learning", "tags": ["Neural Networks", "AI"]}
    ], 'This is a text about AI and Deep Learning.', 
    {"concept_content": "AI and Deep Learning have a close relation.", "concept_tags": "Relation, AI, Deep Learning"},
    'AI and Deep Learning have a close relation.', 
    ['Relation', 'AI', 'Deep Learning']),
    # Add more test cases as needed
])
def test_get_linked_concept_content(mocker, concepts, input_text, mock_data, expected_content, expected_tags):
    # Arrange
    mock_api(mocker, mock_data)

    # Act
    content, tags = get_linked_concept_content(concepts, input_text)
    tags = split_concept_tags(tags)

    # Assert
    assert content == expected_content
    assert tags == expected_tags

@pytest.mark.parametrize("input_text,mock_data,expected", [
    ('This is a text about AI.', {}, False),
    ('', {"title": False}, False),
    # Add other cases as needed
])
def test_get_concept_title_edge_cases(mocker, input_text, mock_data, expected):
    # Arrange
    mock_api(mocker, mock_data)

    # Act
    result = get_concept_title(input_text)

    # Assert
    assert result == expected

@pytest.mark.parametrize("concept,input_text,mock_data,expected_content,expected_tags", [
    ('AI', 'This is a text about AI.', {"concept_content": "AI is the simulation of human intelligence."}, 'AI is the simulation of human intelligence.', False),
    # Add other edge cases as needed
])
def test_get_concept_content_edge_cases(mocker, concept, input_text, mock_data, expected_content, expected_tags):
    # Arrange
    mock_api(mocker, mock_data)

    # Act
    content, tags = get_concept_content(concept, input_text)
    if tags:
        tags = split_concept_tags(tags)

    # Assert
    assert content == expected_content
    assert tags == expected_tags

