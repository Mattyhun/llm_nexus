import sys
import requests
import logging as log
from pyprojroot import here
sys.path.append(str(here()))
from project_config import initialize_logging, HUGGINGFACE_API_KEY

API_URL = "https://api-inference.huggingface.co/models/"


def call_huggingface_api(model, message_content):
    '''
    Call the HuggingFace API with the given message and model, return the response.
    '''
    
    url = API_URL + model

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }

    data = {"inputs": message_content}

    log.debug("Sending request to %s with data: %s", url, data)

    response = requests.post(url, headers=headers, json=data, timeout=60)
    log.debug("Response: %s", response)
    return response

def get_generated_text_from_response(response):
    return response[0]['generated_text']

if __name__ == "__main__":
    initialize_logging()
    model = "gpt2"
    response = call_huggingface_api(
        model, "Generate me a python function that returns the sum of two numbers : def sum(a,b):")

    generated_text = get_generated_text_from_response(response.json())
    print(generated_text)
