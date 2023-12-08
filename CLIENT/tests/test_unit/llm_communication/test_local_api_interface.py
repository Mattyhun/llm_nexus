
from pyprojroot import here
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(str(here()))
from llm_communication.local_api_interface import call_local_api, get_text_from_output

class TestLocalApiInterface(unittest.TestCase):

    @patch('llm_communication.local_api_interface.requests.post')
    def test_call_local_api(self, mock_post):
        # Setup
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "choices": [{"text": "Function to add two numbers"}]
        }
        mock_post.return_value = mock_response
        model = "test-model"
        message_content = "Test message"

        # Test
        response = call_local_api(model, message_content)
        self.assertEqual(response.json(), {
            "choices": [{"text": "Function to add two numbers"}]
        })

    def test_get_text_from_output(self):
        # Test
        output = {"choices": [{"text": "Function to add two numbers"}]}
        result = get_text_from_output(output)
        self.assertEqual(result, "Function to add two numbers")

if __name__ == '__main__':
    unittest.main()
