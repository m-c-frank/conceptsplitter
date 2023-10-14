import openai

# Define the OpenAI API key (replace with yours)
API_KEY = "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"
openai.api_key = API_KEY

SYSTEM_MESSAGE = """
"you are a sophisticated parsing entity, able to capture the distinct nuances of my specific writing style. then you are tasked to extract atomic concepts from the text using <br> to delimit each individual concept. the sum of all concepts should approximately have the same length and feel of the original input. also try to also add a hint of the context of the input text to the extracted individual concepts. remember that the text might just be a text dump from some website. try your best"
"""

with open("concept_split.ppt", "r") as file:
    PREPROMPT = file.read()

def get_concepts(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=[
            {"role": "system", "content": SYSTEM_MESSAGE},
            {"role": "user", "content": prompt},
         ]
    )
    
    return response.choices[0]["message"]["content"]

def split_concepts(concepts):
    """
    Function to split a string of concepts into a list of individual concepts.
    
    Returns:
    - list: A list of individual concepts.
    """
    return concepts.split("\n<br>\n")


def extract_atomic_concepts(text, filename):
    """
    Function to extract atomic concepts from a custom prompt filetype using the OpenAI API.
    
    Returns:
    - str: The extracted and elaborated concepts.
    """
    
    prompt = PREPROMPT + "\n" + text + '\n"""'

    notes = split_concepts(get_concepts(prompt))
    print(notes)

    notes.append(text) 

    print(prompt)

    print(notes)

    return notes

    # Make API call
    # print(prompt)
   



