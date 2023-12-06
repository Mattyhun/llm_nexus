import openai
import requests
import json
import os
import sys
from pyprojroot import here
sys.path.append(str(here()))
from project_config import initialize_logging

OPENAI_API_KEY = "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"

import requests
import logging as log

import time
from functools import wraps



def retry(max_retries=3, backoff_factor=2, retriable_statuses=[500, 503]):
    def decorator_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    response = func(*args, **kwargs)
                    if response.status_code in retriable_statuses:
                        log.warning("Retriable error %s. Attempt %s of %s.", response.status_code, attempt + 1, max_retries)
                        time.sleep(backoff_factor ** attempt)
                        continue
                    return response
                except requests.exceptions.Timeout as e:
                    # Handle timeout error here
                    log.error("Timeout error: %s", e)
                    if attempt < max_retries - 1:
                        log.warning("Retrying... Attempt %s of %s due to timeout.", attempt + 1, max_retries)
                        time.sleep(backoff_factor ** attempt)
                    else:
                        log.error("Max retries reached. No more attempts due to timeout.")
                        return None
                except requests.exceptions.RequestException as e:
                    log.error("Request Exception: %s", e)
                    if attempt < max_retries - 1:
                        log.warning("Retrying... Attempt %s of %s.", attempt + 1, max_retries)
                        time.sleep(backoff_factor ** attempt)
                    else:
                        log.error("Max retries reached. No more attempts.")
                        return None
            return None
        return wrapper
    return decorator_retry

@retry(max_retries=3, backoff_factor=2)
def call_openai_api(message_content, model):
    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    data = {
        "model": model,
        "messages": [{"role": "user", "content": message_content}],
        "temperature": 0.7
    }
    log.debug("Sending request to %s with data: %s", url, data)
    response = requests.post(url, headers=headers, json=data, timeout=30)
    if response.status_code != 200:
        log.error("Error %s: %s", response.status_code, response.text)
    return response

def extract_message_content(response_json):
    # Check if the required keys are in the response
    if 'choices' in response_json and len(response_json['choices']) > 0:
        message = response_json['choices'][0].get('message', {})
        if 'content' in message:
            return message['content']
        else:
            return "No content found in message."
    else:
        return "No choices found in response."
    
#TODO: Handle no internet connection

if __name__ == "__main__":
    initialize_logging()
    # Example usage
    response = call_openai_api("Create a python function that says hello world","gpt-3.5-turbo")
    if response and response.status_code == 200:
        print("Successful response.")
    else:
        print("Failed to get a successful response.")

    print(extract_message_content(response.json()))