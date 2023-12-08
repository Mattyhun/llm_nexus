import unittest
from unittest.mock import patch
import sys
from pyprojroot import here
sys.path.append(str(here()))
from main import main

class TestMainFunction(unittest.TestCase):
    @patch('main.read_problems')
    @patch('main.generate_answers_parallelized')
    @patch('main.write_jsonl')
    @patch('main.read_and_print_jsonl')
    def test_basic_functionality(self, mock_read_and_print, mock_write, mock_generate, mock_read):
        # Beállítja a mock objektumokat, hogy csak a main funkció logikáját tesztelje
        mock_read.return_value = {"problem1": {"prompt": "Example prompt"}}
        mock_generate.return_value = [{"task_id": "problem1", "completion": "Example completion"}]

        # Hívja a main funkciót teszt paraméterekkel
        main("test_interface", "test_model")

        # Ellenőrzi, hogy a mockolt funkciókat helyesen hívta-e meg
        mock_read.assert_called_once()
        mock_generate.assert_called_once()
        mock_write.assert_called_once()
        mock_read_and_print.assert_called_once()
