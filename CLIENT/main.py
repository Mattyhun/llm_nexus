import logging as log
from project_config import initialize_logging
from generate_samples import generate_answer_samples
from utility.get_pass_k_value import get_pass_k_value
from utility.validate_file_path import validate_file_path
from utility.data_handler import read_problems, write_jsonl
from utility.calculate_optimal_threads import calculate_optimal_threads
from vm_communication.vm_communication import run_command_on_vm, transfer_file_to_vm


def main():
    initialize_logging()
    log.info("Starting the main function")
    samples_file_path = "samples.jsonl"
    model = "gpt-3.5-turbo"
    problems = read_problems()

    # send_query_to_model()
    optimal_number_of_threads = calculate_optimal_threads()
    try:
        samples = generate_answer_samples(
            model, problems, num_samples_per_task=1, max_threads=optimal_number_of_threads, requests_per_minute=3500)
    except Exception as e:
        log.error("Failed to generate samples: %s", e)
        raise RuntimeError("Failed to generate samples") from e

    write_jsonl(samples_file_path, samples)

    # send_code_result_to_testing_vm()
    if not validate_file_path(samples_file_path):
        raise RuntimeError("Failed to validate samples file path")

    samples_destination_path = "testsamples.jsonl"
    transfer_file_to_vm(samples_file_path, samples_destination_path)

    # initiate_testing_on_vm()
    vm_output = run_command_on_vm(
        f"python3 human-eval/human_eval/evaluate_functional_correctness.py {samples_destination_path}")
    test_result = get_pass_k_value(vm_output)

    log.info("test results:\n")
    log.info(test_result)


if __name__ == "__main__":
    main()
