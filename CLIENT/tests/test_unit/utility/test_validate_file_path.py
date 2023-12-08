
from pyprojroot import here
import sys
import os
import tempfile
import unittest
from unittest.mock import patch
sys.path.append(str(here()))
from utility.validate_file_path import validate_file_path

class TestValidateFilePath(unittest.TestCase):

    def setUp(self):
        # Setup a temporary file and directory for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False).name
        with open(self.temp_file, 'w') as f:
            f.write("Sample content")  # Ensure the file is not empty

        # Creating a temporary directory
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Cleanup the temporary file and directory after tests
        os.remove(self.temp_file)
        os.rmdir(self.temp_dir)

    def test_valid_file_path(self):
        # Test with a valid file path
        self.assertTrue(validate_file_path(self.temp_file))

    def test_invalid_file_path_nonexistent(self):
        # Test with a nonexistent file path
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.txt")
        self.assertFalse(validate_file_path(nonexistent_file))

    def test_invalid_file_path_directory(self):
        # Test with a directory path instead of a file
        self.assertFalse(validate_file_path(self.temp_dir))

    def test_invalid_file_path_empty(self):
        # Test with an empty file
        empty_file = tempfile.NamedTemporaryFile(delete=False).name
        self.assertFalse(validate_file_path(empty_file))
        os.remove(empty_file)

    @patch('utility.validate_file_path.log')
    def test_logging(self, mock_log):
        # Test the logging for a valid file
        validate_file_path(self.temp_file)
        mock_log.info.assert_called_once()

        # Reset mock
        mock_log.reset_mock()

        # Test the logging for an invalid file
        empty_file = tempfile.NamedTemporaryFile(delete=False).name
        validate_file_path(empty_file)
        mock_log.error.assert_called()
        os.remove(empty_file)

if __name__ == '__main__':
    unittest.main()
