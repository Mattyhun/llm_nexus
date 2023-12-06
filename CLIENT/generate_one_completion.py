import requests
import json
from llm_communication.openai_api_interface import call_openai_api, extract_message_content
import logging as log

# TODO: make this flexible

def generate_one_completion(model, prompt):
    """
    Generate one completion from the given prompt and model returns the response content
    """
    response = call_openai_api(model, prompt)
    response_content = extract_message_content(response.json())
    log.debug(response_content)
    return response_content

if __name__ == "__main__":

    response = generate_one_completion("gpt-3.5-turbo","Implement a function that returns the sum of two numbers")
    print(response)


