
from pyprojroot import here
import sys
import unittest
from unittest.mock import patch, MagicMock
sys.path.append(str(here()))
from llm_communication.openai_api_interface import call_openai_api, extract_message_content, handle_error_response

class TestOpenaiApiInterface(unittest.TestCase):

    @patch('llm_communication.openai_api_interface.requests.post')
    def test_call_openai_api_success(self, mock_post):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [{"message": {"content": "Hello World"}}]
        }
        mock_post.return_value = mock_response
        model = "gpt-3.5-turbo"
        message_content = "Test message"

        # Test
        response = call_openai_api(model, message_content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "choices": [{"message": {"content": "Hello World"}}]
        })

    @patch('llm_communication.openai_api_interface.requests.post')
    def test_call_openai_api_failure(self, mock_post):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response
        model = "gpt-3.5-turbo"
        message_content = "Test message"

        # Test & Assert
        with self.assertRaises(RuntimeError):
            call_openai_api(model, message_content)

    def test_extract_message_content(self):
        # Test
        response_json = {"choices": [{"message": {"content": "Hello World"}}]}
        result = extract_message_content(response_json)
        self.assertEqual(result, "Hello World")

    def test_extract_message_content_no_content(self):
        # Test
        response_json = {"choices": [{}]}
        result = extract_message_content(response_json)
        self.assertEqual(result, "No content found in message.")

if __name__ == '__main__':
    unittest.main()
