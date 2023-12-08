import unittest
import logging
import sys
from pyprojroot import here
sys.path.append(str(here()))
from generate_answers_parallelized import generate_answers_parallelized
from utility.data_handler import read_problems

class TestGenerateAnswersParallelized(unittest.TestCase):
    def setUp(self):
        """ Tesztkörnyezet előkészítése. """
        self.model = 'gpt-3.5-turbo'  
        self.problems = read_problems()  
        self.num_samples_per_task = 1
        self.max_threads = 10  
        self.interface = "openai"

    def test_parallel_generation(self):
        """ Teszteljük a generate_answers_parallelized funkciót. """
        logging.info("Tesztelés indítása a generate_answers_parallelized modullal.")
        samples = generate_answers_parallelized(self.interface, self.model, self.problems, self.num_samples_per_task, self.max_threads)

        # Ellenőrizzük, hogy minden feladat sikeresen befejeződött-e
        self.assertEqual(len(samples), len(self.problems) * self.num_samples_per_task,
                         "Nem minden feladat fejeződött be sikeresen.")

if __name__ == '__main__':
    unittest.main()
