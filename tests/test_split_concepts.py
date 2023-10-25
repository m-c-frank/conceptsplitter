import pytest
import json
from your_file_name import (  # replace with the name of your file
    split_concept_titles,
    split_concept_tags,
    get_concept_title,
    get_concept_titles,
    get_concept_content,
    get_linked_concept_content
)

def test_split_concept_titles():
    result = split_concept_titles({'concept_titles': 'AI, Neural Networks, Deep Learning'})
    assert result == ['AI', 'Neural Networks', 'Deep Learning']

def test_split_concept_tags():
    result = split_concept_tags('AI, Neural Networks, Deep Learning')
    assert result == ['AI', 'Neural Networks', 'Deep Learning']

def test_get_concept_title(mocker):
    mock_choice = {
        "message": {
            "function_call": {
                "arguments": json.dumps({"title": "AI Intro"})
            }
        }
    }
    mocker.patch('your_file_name.neuralapi.ChatCompletion.create', return_value=Mock(choices=[mock_choice]))
    result = get_concept_title('This is a text about AI.')
    assert result == 'AI Intro'

def test_get_concept_titles(mocker):
    mock_choice = {
        "message": {
            "function_call": {
                "arguments": json.dumps({"concept_titles": "AI, Neural Networks"})
            }
        }
    }
    mocker.patch('your_file_name.neuralapi.ChatCompletion.create', return_value=Mock(choices=[mock_choice]))
    result = get_concept_titles('This is a text about AI and Neural Networks.')
    assert result == ['AI', 'Neural Networks']

def test_get_concept_content(mocker):
    mock_choice = {
        "message": {
            "function_call": {
                "arguments": json.dumps({
                    "concept_content": "AI is the simulation of human intelligence.",
                    "concept_tags": "Simulation, Intelligence"
                })
            }
        }
    }
    mocker.patch('your_file_name.neuralapi.ChatCompletion.create', return_value=Mock(choices=[mock_choice]))
    content, tags = get_concept_content('AI', 'This is a text about AI.')
    assert content == 'AI is the simulation of human intelligence.'
    assert tags == ['Simulation', 'Intelligence']

def test_get_linked_concept_content(mocker):
    mock_choice = {
        "message": {
            "function_call": {
                "arguments": json.dumps({
                    "concept_content": "AI and Deep Learning have a close relation.",
                    "concept_tags": "Relation, AI, Deep Learning"
                })
            }
        }
    }
    mocker.patch('your_file_name.neuralapi.ChatCompletion.create', return_value=Mock(choices=[mock_choice]))
    concepts = [
        {"title": "AI", "tags": ["Tech", "Intelligence"]},
        {"title": "Deep Learning", "tags": ["Neural Networks", "AI"]}
    ]
    content, tags = get_linked_concept_content(concepts, 'This is a text about AI and Deep Learning.')
    assert content == 'AI and Deep Learning have a close relation.'
    assert tags == ['Relation', 'AI', 'Deep Learning']

