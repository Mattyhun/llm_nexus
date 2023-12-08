import sys
import requests
import logging as log
from pyprojroot import here
sys.path.append(str(here()))
from project_config import initialize_logging, HOSTED_API_ENDPONT



def call_local_api(model, message_content, url=HOSTED_API_ENDPONT):
    '''Call the OpenAI API with the given message and model, return the response.'''
    headers = {"Content-Type": "application/json",
               "Authorization": "Bearer not needed for a local LLM"}
    data = {
        "model": model, 
        "temperature": 0.28,
        "max_tokens": 200,
        "top_p": 0.95,
        "n": 1,
        "echo": True,
        "stream": False,
        "prompt": message_content
        }

    log.debug("Sending request to %s with data: %s", url, data)

    response = requests.post(url, headers=headers, json=data, timeout=90)
    log.debug(response.json())
    return response

def get_text_from_output(output):
    return output['choices'][0]['text']

if __name__ == "__main__":
    initialize_logging()

    response = call_local_api("wizardlm-13b-v1.2.Q4_0.gguf", "Create me a python function that adds two numbers together.")
    response_text = get_text_from_output(response.json())
    print(response_text)
