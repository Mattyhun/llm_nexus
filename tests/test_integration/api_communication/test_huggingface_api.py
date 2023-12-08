import unittest
import requests
import sys
from pyprojroot import here
sys.path.append(str(here()))
from project_config import HUGGINGFACE_API_KEY

class TestHuggingfaceAPI(unittest.TestCase):
    def test_valid_request(self):
        url = "https://api-inference.huggingface.co/models/gpt2"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }
        data = {"inputs": "Hello"}
        response = requests.post(url, headers=headers, json=data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_request(self):
        url = "https://api-inference.huggingface.co/models/invalid-model"
        headers = {
            "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"
        }
        data = {"inputs": "Hello"}
        response = requests.post(url, headers=headers, json=data)
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
