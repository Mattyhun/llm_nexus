import json
import os
from calculate_optimal_threads import calculate_optimal_threads
from generate_samples import generate_answer_samples
from human_eval.data import read_problems, write_jsonl
from vm_communication import run_command_on_vm, transfer_file_to_vm, validate_file_path
from project_config import initialize_logging
import logging as log

def main():
    initialize_logging()  
    samples_file_path = "samples.jsonl"
    # select_model()

    problems = read_problems()


    # send_query_to_model()
    optimal_number_of_threads = calculate_optimal_threads()
    samples = generate_answer_samples(problems, num_samples_per_task=1, max_threads=optimal_number_of_threads, requests_per_minute=3500)
    write_jsonl(samples_file_path, samples)


    # send_code_result_to_testing_vm()
    if not validate_file_path(samples_file_path):
        raise RuntimeError("Failed to validate samples file path")
    
    samples_destination_path = "testsamples.jsonl"
    transfer_file_to_vm(samples_file_path, samples_destination_path)

    # initiate_testing_on_vm()
    testing_result = run_command_on_vm(f"python3 human-eval/human_eval/evaluate_functional_correctness.py {samples_destination_path}")

    log.info("testing results:\n%s",testing_result)


if __name__ == "__main__":
    main()