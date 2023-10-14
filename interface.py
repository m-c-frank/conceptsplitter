import openai

# Define the OpenAI API key (replace with yours)
API_KEY = "YOUR_OPENAI_API_KEY"
openai.api_key = API_KEY

def extract_atomic_concepts_from_custom_file():
    """
    Function to extract atomic concepts from a custom prompt filetype using the OpenAI API.
    
    Returns:
    - str: The extracted and elaborated concepts.
    """
    
    # Read the instruction from custom prompt filetype (assuming it's named custom_prompt.txt for now)
    with open("custom_prompt.txt", "r") as file:
        content = file.read()

    # Extract the specific input string for transformation from the content
    start_index = content.find("now try again and apply it to the following input string") + len("now try again and apply it to the following input string (the new text you should transform):")
    end_index = content.find("ChatGPT")
    input_string = content[start_index:end_index].strip()

    # Create the combined prompt with the instruction and input string
    prompt = content + "\n" + input_string

    # Make API call
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        prompt=prompt,
        max_tokens=500  # You can adjust this as needed
    )
    
    return response.choices[0].text.strip()

if __name__ == "__main__":
    extracted_concepts = extract_atomic_concepts_from_custom_file()
    print(extracted_concepts)
