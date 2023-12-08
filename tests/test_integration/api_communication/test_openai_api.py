import unittest
import requests
import sys
from pyprojroot import here
sys.path.append(str(here()))
from project_config import OPENAI_API_KEY

class TestOpenAIAPI(unittest.TestCase):
    def test_valid_request(self):
        url = "https://api.openai.com/v1/engines"
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}"
        }
        response = requests.get(url, headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_invalid_request(self):
        url = "https://api.openai.com/v1/engines"
        headers = {
            "Authorization": "Bearer invalid_key"
        }
        response = requests.get(url, headers=headers)
        self.assertNotEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
