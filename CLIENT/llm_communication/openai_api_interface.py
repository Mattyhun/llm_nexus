import requests
import sys
import logging as log
import time
from functools import wraps
from pyprojroot import here
sys.path.append(str(here()))
from project_config import initialize_logging, OPENAI_API_KEY


def retry(max_retries=3, backoff_factor=2, retriable_statuses={500, 503, 429}):
    '''Decorator factory to retry a function call in case of a retriable exception or status code.'''

    def decorator_retry(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    response = func(*args, **kwargs)

                    if response and response.status_code in retriable_statuses:
                        log.warning("Retriable status %s. Attempt %s of %s.",
                                    response.status_code, attempt + 1, max_retries)
                        time.sleep(backoff_factor ** attempt)
                        continue

                    return response

                except requests.exceptions.RequestException as e:
                    handle_request_exception(
                        e, attempt, max_retries, backoff_factor)

            return None

        return wrapper

    return decorator_retry


def handle_request_exception(exception, attempt, max_retries, backoff_factor):
    '''Handle a request exception.'''
    log.error(f"Request Exception: {exception}")

    if attempt < max_retries - 1:
        log.warning(f"Retrying... Attempt {attempt + 1} of {max_retries}.")
        time.sleep(backoff_factor ** attempt)
    else:
        log.error("Max retries reached. No more attempts.")


@retry(max_retries=3, backoff_factor=2)
def call_openai_api(model, message_content):
    '''Call the OpenAI API with the given message and model, return the response.'''
    url = "https://api.openai.com/v1/chat/completions"
    headers = {"Content-Type": "application/json",
               "Authorization": f"Bearer {OPENAI_API_KEY}"}
    data = {"model": model, "messages": [
        {"role": "user", "content": message_content}], "temperature": 0.7}

    log.debug("Sending request to %s with data: %s", url, data)

    response = requests.post(url, headers=headers, json=data, timeout=30)

    if response and response.status_code != 200:
        handle_error_response(response)

    return response


def handle_error_response(response):
    fatal_errors = {
        401: "Unauthorized. Check your OpenAI API key.",
        404: "Endpoint not found. Check your OpenAI API endpoint."
    }

    error_message = fatal_errors.get(response.status_code)

    if error_message:
        log.error(error_message)
        raise RuntimeError(error_message)

    log.error("Error %s: %s", response.status_code, response.text)


def extract_message_content(response_json):
    '''Extract the message content from the response JSON.'''
    choices = response_json.get('choices', [])

    if choices:
        message_content = choices[0].get('message', {}).get('content')

        if message_content:
            return message_content

    return "No content found in message."


if __name__ == "__main__":
    initialize_logging()

    response = call_openai_api(
        "gpt-3.5-turbo", "Create a python function that says hello world")

    if response and response.status_code == 200:
        print("Successful response.")
    else:
        print("Failed to get a successful response.")

    print(extract_message_content(response.json()))
