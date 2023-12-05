import requests
import json
import os

class LLMCommunicator:
    def __init__(self):
        self.api_key = os.getenv('LLM_API_KEY')
        self.api_url = 'https://api.openai.com/v1/engines/davinci-codex/completions'

    def send_request(self, prompt):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'prompt': prompt,
            'max_tokens': 100
        }
        response = requests.post(self.api_url, headers=headers, json=data)
        return response.json()

class DatasetManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_test_cases(self):
        with open(self.file_path, 'r') as file:
            data = json.load(file)
        return data

def send_code_to_tester(code, tester_url):
    # Ezt a függvényt tovább lehet fejleszteni a GCP VM kommunikációval
    response = requests.post(tester_url, data={'code': code})
    return response.text

# Példa használat
communicator = LLMCommunicator()
dataset_manager = DatasetManager('path_to_dataset.json')
test_cases = dataset_manager.get_test_cases()

for test in test_cases:
    prompt = test['prompt']
    response = communicator.send_request(prompt)
    code = response['choices'][0]['text']
    test_result = send_code_to_tester(code, 'http://your_tester_vm_url')
    print(test_result)
