import argparse
import logging as log
from project_config import initialize_logging
from generate_samples import generate_answer_samples
from utility.get_pass_k_value import get_pass_k_value
from utility.validate_file_path import validate_file_path
from utility.calculate_optimal_threads import calculate_optimal_threads
from utility.data_handler import read_problems, sort_jsonl, write_jsonl, read_and_print_jsonl
from vm_communication.vm_communication import run_command_on_vm, transfer_file_from_vm, transfer_file_to_vm


def main(interface, model, num_samples_per_task=1, requests_per_minute=3500):
    initialize_logging()
    log.info("Starting the main function")
    samples_file_path = "samples.jsonl"
    samples_destination_path = "samples.jsonl"
    results_file_path = "result.jsonl"

    problems = read_problems()

    optimal_number_of_threads = calculate_optimal_threads()
    
    try:
        samples = generate_answer_samples(
            interface, model, problems, num_samples_per_task, max_threads=optimal_number_of_threads, requests_per_minute=requests_per_minute)
    except Exception as e:
        log.error("Failed to generate samples: %s", e)
        raise RuntimeError("Failed to generate samples") from e

    write_jsonl(samples_file_path, samples)

    if not validate_file_path(samples_file_path):
        raise RuntimeError("Failed to validate samples file path")

    transfer_file_to_vm(samples_file_path, samples_destination_path)

    # Initiate testing on the VM
    log.info("Running tests on the VM")
    vm_output = run_command_on_vm(
        f"python3 human-eval/human_eval/evaluate_functional_correctness.py {samples_destination_path}")
    
    pass_k_value = get_pass_k_value(vm_output)

    transfer_file_from_vm(samples_destination_path + "_results.jsonl", results_file_path)

    sort_jsonl(results_file_path)

    log.info("test results:\n")
    read_and_print_jsonl(results_file_path)
    
    log.info("pass k value:")
    log.info(pass_k_value)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='This script requires a model and interface as input. Please provide both. \n For example: python main.py --model wizardlm-13b-v1.2.Q4_0.gguf --interface local \n Or: \n python main.py --model "gpt-3.5-turbo" --interface "openai" --num_samples_per_task 1 --requests_per_minute 3500',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--model', type=str, required=True, help='The model to be used for evaluation.')
    parser.add_argument('--interface', type=str, required=True, help='The interface to be used. possible values: local, huggingface, openai')
    parser.add_argument('--num_samples_per_task', type=int, default=1, help='Number of samples generated per task.')
    parser.add_argument('--requests_per_minute', type=int, default=3500, help='Number of api requests per minute.')
    args = parser.parse_args()
    main(args.interface, args.model, args.num_samples_per_task, args.requests_per_minute)