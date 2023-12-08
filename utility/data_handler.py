from typing import Iterable, Dict
import gzip
import json
import os
import sys
import logging as log
from pyprojroot import here
sys.path.append(str(here()))

ROOT = str(here())
HUMAN_EVAL = os.path.join(ROOT, "data", "HumanEval.jsonl.gz")


def read_problems(evalset_file: str = HUMAN_EVAL) -> Dict[str, Dict]:
    '''
    Parses the human eval file and returns a dictionary of tasks
    '''
    return {task["task_id"]: task for task in stream_jsonl(evalset_file)}


def stream_jsonl(filename: str) -> Iterable[Dict]:
    """
    Parses each jsonl line and yields it as a dictionary
    """
    if filename.endswith(".gz"):
        with open(filename, "rb") as gzfp:
            with gzip.open(gzfp, 'rt') as fp:
                for line in fp:
                    if any(not x.isspace() for x in line):
                        yield json.loads(line)
    else:
        with open(filename, "r") as fp:
            for line in fp:
                if any(not x.isspace() for x in line):
                    yield json.loads(line)


def write_jsonl(filename: str, data: Iterable[Dict], append: bool = False):
    """
    Writes an iterable of dictionaries to jsonl
    """
    if append:
        mode = 'ab'
    else:
        mode = 'wb'
    filename = os.path.expanduser(filename)
    if filename.endswith(".gz"):
        with open(filename, mode) as fp:
            with gzip.GzipFile(fileobj=fp, mode='wb') as gzfp:
                for x in data:
                    gzfp.write((json.dumps(x) + "\n").encode('utf-8'))
    else:
        with open(filename, mode) as fp:
            for x in data:
                fp.write((json.dumps(x) + "\n").encode('utf-8'))

def read_and_print_jsonl(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            task_id = data.get('task_id', '')
            result = data.get('result', '')
            passed = data.get('passed', '')

            log.info('Task ID: %s', task_id)
            log.info('Result: %s', result)
            log.info('Passed: %s ', passed)
            log.info("--------------------------------------------")


def sort_jsonl(file_path):
    '''Sorts the jsonl file based on the numeric part of the task_id in ascending order'''
    with open(file_path, 'r') as f:
        data = [json.loads(line) for line in f]

    # Sort the data list based on the numeric part of the task_id in ascending order
    data.sort(key=lambda x: int(x['task_id'].split('/')[1]))

    # Overwrite the sorted data back into the file
    with open(file_path, 'w') as f:
        for entry in data:
            json.dump(entry, f)
            f.write('\n')

