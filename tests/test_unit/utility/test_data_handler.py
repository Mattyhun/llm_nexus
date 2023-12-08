
from pyprojroot import here
import sys
sys.path.append(str(here()))
import json
import os
import tempfile
import unittest
from unittest.mock import patch, mock_open
from utility.data_handler import read_problems, stream_jsonl, write_jsonl, read_and_print_jsonl, sort_jsonl

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        # Setup a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl").name
        self.temp_file_gz = tempfile.NamedTemporaryFile(delete=False, suffix=".jsonl.gz").name
        self.sample_data = [{"task_id": "task/1", "result": "pass", "passed": True},
                            {"task_id": "task/2", "result": "fail", "passed": False}]

        with open(self.temp_file, 'w') as f:
            for item in self.sample_data:
                json.dump(item, f)
                f.write('\n')

    def tearDown(self):
        # Cleanup the temporary files after tests
        os.remove(self.temp_file)
        if os.path.exists(self.temp_file_gz):
            os.remove(self.temp_file_gz)

    def test_read_problems(self):
        # Test the read_problems function
        problems = read_problems(self.temp_file)
        self.assertEqual(len(problems), 2)
        self.assertIn("task/1", problems)
        self.assertIn("task/2", problems)

    def test_stream_jsonl(self):
        # Test the stream_jsonl function
        data = list(stream_jsonl(self.temp_file))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["task_id"], "task/1")
        self.assertEqual(data[1]["task_id"], "task/2")

    def test_write_jsonl(self):
        # Test the write_jsonl function
        write_jsonl(self.temp_file_gz, self.sample_data, append=False)
        self.assertTrue(os.path.exists(self.temp_file_gz))

    def test_read_and_print_jsonl(self):
        # Test the read_and_print_jsonl function
        with patch('utility.data_handler.log') as mock_log:
            read_and_print_jsonl(self.temp_file)
            self.assertEqual(mock_log.info.call_count, 8)  # 4 lines per entry

    def test_sort_jsonl(self):
        # Test the sort_jsonl function
        unsorted_data = [{"task_id": "task/2", "result": "fail", "passed": False},
                         {"task_id": "task/1", "result": "pass", "passed": True}]
        with open(self.temp_file, 'w') as f:
            for item in unsorted_data:
                json.dump(item, f)
                f.write('\n')

        sort_jsonl(self.temp_file)

        with open(self.temp_file, 'r') as f:
            sorted_data = [json.loads(line) for line in f]

        self.assertEqual(sorted_data[0]["task_id"], "task/1")
        self.assertEqual(sorted_data[1]["task_id"], "task/2")

if __name__ == '__main__':
    unittest.main()
