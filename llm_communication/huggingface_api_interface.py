import requests
import os
import sys
from pyprojroot import here
sys.path.append(str(here()))
from project_config import initialize_logging, HUGGINGFACE_API_KEY
import logging as log

API_URL = "https://api-inference.huggingface.co/models/"


def call_huggingface_api(model, message_content):
    url = API_URL + model

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
    }

    data = {"inputs": message_content}
	
   
    

    log.debug("Sending request to %s with data: %s", url, data)

    response = requests.post(url, headers=headers, json=data, timeout=30)
    log.debug("Response: %s", response)
    return response.json()





if __name__ == "__main__":
    initialize_logging()
    model = "codeparrot/codeparrot"
    response = call_huggingface_api(model, "Generate me a python function that returns the sum of two numbers : def sum(a,b):")

    print(response)

