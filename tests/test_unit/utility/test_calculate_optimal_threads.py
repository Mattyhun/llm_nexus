import logging
import multiprocessing
from unittest.mock import patch
import pytest
import sys
from pyprojroot import here
sys.path.append(str(here()))

from utility.calculate_optimal_threads import calculate_optimal_threads  

def test_default_behavior():
    expected_threads = multiprocessing.cpu_count() * 5
    assert calculate_optimal_threads() == expected_threads

def test_custom_factor():
    factor = 10
    expected_threads = multiprocessing.cpu_count() * factor
    assert calculate_optimal_threads(factor) == expected_threads

def test_zero_factor():
    assert calculate_optimal_threads(0) == 0

def test_negative_factor():
    factor = -5
    expected_threads = multiprocessing.cpu_count() * factor
    assert calculate_optimal_threads(factor) == expected_threads

@patch('utility.calculate_optimal_threads.log')
def test_logging(mock_log):
    calculate_optimal_threads()
    mock_log.info.assert_called_once()
