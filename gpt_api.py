

import requests
import json

def call_openai_api(message_content):
    # Replace with your actual OpenAI API key
    OPENAI_API_KEY = "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"

    # Endpoint for the API
    url = "https://api.openai.com/v1/chat/completions"

    # Headers including the Authorization token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # Data to be sent in the request
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": message_content}],
        "temperature": 0.7
    }

    # Making a POST request to the API
    response = requests.post(url, headers=headers, json=data)

    # Returning the response
    return response.json()

def generate_one_completion(prompt):
    response = call_openai_api(prompt)
    response_content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
    print(response_content)
    return response_content

if __name__ == "__main__":

    response = call_openai_api("Implement a function that returns the sum of two numbers")
    print(response)

    response_content = response.get('choices', [{}])[0].get('message', {}).get('content', '')

    print(response_content)


