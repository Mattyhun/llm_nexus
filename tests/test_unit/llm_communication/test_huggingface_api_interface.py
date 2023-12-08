
from pyprojroot import here
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(str(here()))
from llm_communication.huggingface_api_interface import call_huggingface_api, get_generated_text_from_response

class TestHuggingfaceApiInterface(unittest.TestCase):

    @patch('llm_communication.huggingface_api_interface.requests.post')
    def test_call_huggingface_api(self, mock_post):
        # Setup
        mock_response = MagicMock()
        mock_response.json.return_value = [{"generated_text": "test response"}]
        mock_post.return_value = mock_response
        model = "gpt2"
        message_content = "Test message"

        # Test
        response = call_huggingface_api(model, message_content)
        self.assertEqual(response.json(), [{"generated_text": "test response"}])

    def test_get_generated_text_from_response(self):
        # Test
        response = [{"generated_text": "test response"}]
        result = get_generated_text_from_response(response)
        self.assertEqual(result, "test response")

if __name__ == '__main__':
    unittest.main()
