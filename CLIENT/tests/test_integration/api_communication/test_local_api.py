import unittest
import requests
from pyprojroot import here
import sys
sys.path.append(str(here()))
from project_config import HOSTED_API_ENDPONT

class TestLocalAPI(unittest.TestCase):
    def test_valid_request(self):
        url = HOSTED_API_ENDPONT
        data = {
            "model": "wizardlm-13b-v1.2.Q4_0.gguf", 
            "prompt": "Hello",
            "temperature": 0.28,
            "max_tokens": 200,
            "top_p": 0.95,
            "n": 1,
            "echo": True,
            "stream": False
        }

        response = requests.post(url, json=data, timeout=90)
        self.assertEqual(response.status_code, 200)

    def test_invalid_request(self):
        url = HOSTED_API_ENDPONT
        # Sending invalid model name
        data = {
            "model": "invalid-model", 
            "prompt": "Hello",
            "temperature": 0.7
        }
        response = requests.post(url, json=data, timeout=90)
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
