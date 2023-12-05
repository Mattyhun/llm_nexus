import requests

class LLMCommunicator:
    def __init__(self, api_key, base_url, model):
        self.api_key = api_key
        self.base_url = base_url
        self.model = model

    def send_request(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 100
        }
        api_url = f"{self.base_url}/{self.model}/completions"
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()
