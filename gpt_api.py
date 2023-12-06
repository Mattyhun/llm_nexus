import requests
import json
from llm_communication.openai_api_interface import call_openai_api, extract_message_content
import logging as log


def generate_one_completion(prompt):
    response = call_openai_api(prompt, "gpt-3.5-turbo")
    response_content = extract_message_content(response.json())
    log.debug(response_content)
    return response_content

if __name__ == "__main__":

    response = generate_one_completion("Implement a function that returns the sum of two numbers")
    print(response)

    # response_content = response.get('choices', [{}])[0].get('message', {}).get('content', '')

    # print(response_content)


