import neuralapi
import re
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

# Fetch the neuralapi API key from environment variable
API_KEY = os.environ.get("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY in the .env file.")
neuralapi.api_key = API_KEY


SYSTEM_MESSAGE = """
you are a sophisticated parsing entity, able to capture the distinct nuances of my specific writing style. then you are tasked to extract atomic concepts from the text. the sum of all concepts should approximately have the same length and feel of the original input. remember that the text might just be a text dump from some website. try your best
"""

SYSTEM_MESSAGE_TITLE = """
you are a sophisticated parsing entity, your task is to just find a nice short but concise title for some text which will be provided to you.
"""

SYSTEM_MESSAGE_CONTENT = """
you are a sophisticated parsing entity. you are tasked to extract atomic concepts from the text based on the name of a concept and the context which will be provided.
"""

SYSTEM_MESSAGE_LINKER = """
you are a sophisticated parsing entity. you are tasked with identifying and explaining the links between concepts in a source document in a clear and concise manner with the given information. Never just state that they are linked. Instead reimagine how they are linked in a creative way. Imagine how you are drawing from you vast knowledge and identify novel ways on how the concepts are linked.
"""



def split_concept_titles(concept_titles):
    # example input : {'concept_titles': 'AI Simple Tags, Explaining Chain of Thoughts, Saving Associations'}
    if not concept_titles:
        return concept_titles
    return [i.strip() for i in concept_titles["concept_titles"].split(",")]

def split_concept_tags(concept_tags):
    if not concept_tags:
        return concept_tags
    # example input : {'concept_tags': 'AI Simple Tags, Explaining Chain of Thoughts, Saving Associations'}
    return [i.strip() for i in concept_tags.split(",")]


def get_concept_title(text):
    prompt = f"I need to find a title for the following text. Please make sure its concise and clear. Rarely use more than 4 words. The text in question: {text}"
    response = neuralapi.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE_TITLE},
            {"role": "user", "content": prompt},
        ],
        functions=[
            {
                "name": "write_title",
                "description": "takes the title and writes it to the index",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "The concise and clear title which perfectly matches the texts content.",
                        },
                    },
                },
                "required": ["title"],
            },
        ],
        function_call={"name": "write_title"},
    )

    title = json.loads(response.choices[0]["message"]["function_call"]["arguments"]).get("title", False)
    return title if title else False


def get_concept_titles(prompt):
    response = neuralapi.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
        ],
        functions=[
            {
                "name": "process_atomic_concepts",
                "description": "takes the names of the extracted atomic concepts and processes them further.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "concept_titles": {
                            "type": "string",
                            "description": "The main but abstracted concepts within the provided text. Short but clear titles and comma delimited.",
                        },
                    },
                },
                "required": ["concept_titles"],
            },
        ],
        function_call={"name": "process_atomic_concepts"},
    )



    return json.loads(response.choices[0]["message"]["function_call"]["arguments"])


def get_concept_content(concept_title, source_context):
    prompt = f"The title of the concept i want you to explain is {concept_title}. Explain it fundamentally, only use the context to see how it could be applied. The context was: {source_context}"
    response = neuralapi.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE_CONTENT},
            {"role": "user", "content": prompt},
        ],
        functions=[
            {
                "name": "write_concept_to_file",
                "description": "takes the description or definition of a concept and writes it to a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "concept_content": {
                            "type": "string",
                            "description": "Approximately 100 words which explains the concept.",
                        },
                        "concept_tags": {
                            "type": "string",
                            "description": "3 to 10 single word tags that describe the content of this concept. Must be comma separated.",
                        },
                    },
                },
                "required": ["concept_content", "concept_tags"],
            },
        ],
        function_call={"name": "write_concept_to_file"},
    )

    concept_content = json.loads(
        response.choices[0]["message"]["function_call"]["arguments"]
    ).get("concept_content", False)

    concept_tags = json.loads(
        response.choices[0]["message"]["function_call"]["arguments"]
    ).get("concept_tags", False)

    return concept_content, concept_tags


def get_linked_concept_content(concepts, source_context):
    concepts_info = "\n".join(
        [f"title: {concept['title']}, tags: {concept['tags']}" for concept in concepts]
    )

    prompt = f"""Okay so please with the following information on the concepts ({concepts_info}); i have extracted from the source context ({source_context}). please identify a nice and elegant way on how the concepts were linked in the source context"""

    response = neuralapi.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE_LINKER},
            {"role": "user", "content": prompt},
        ],
        functions=[
            {
                "name": "write_to_file",
                "description": "takes a linked concept note and writes it to a file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "concept_content": {
                            "type": "string",
                            "description": "Approximately 100 words in which the links between the given concepts are explained using the source document and additional information.",
                        },
                        "concept_tags": {
                            "type": "string",
                            "description": "3 to 10 single word tags that describe the content of this new linked concept. Must be comma separated.",
                        },
                    },
                },
                "required": ["concept_content", "concept_tags"],
            },
        ],
        function_call={"name": "write_to_file"},
    )

    concept_content = json.loads(
        response.choices[0]["message"]["function_call"]["arguments"]
    ).get("concept_content", False)
    concept_tags = json.loads(
        response.choices[0]["message"]["function_call"]["arguments"]
    ).get("concept_tags", False)

    return concept_content, concept_tags
