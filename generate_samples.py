from concurrent.futures import ThreadPoolExecutor, as_completed
from calculate_optimal_threads import calculate_optimal_threads
from human_eval.data import write_jsonl, read_problems
from gpt_api import generate_one_completion
import logging as log
from project_config import initialize_logging
import time  # Import the time module

# TODO: Optimize max_threads

def generate_answer_samples(problems, num_samples_per_task=1, max_threads=50, requests_per_minute=3500):
    # Calculate delay between requests to adhere to the rate limit
    delay_between_requests = 60 / requests_per_minute  # in seconds

    # Function to generate samples for a single task
    def generate_task_samples(task_id):
        log.info("Generating samples for task %s", task_id)
        return {
            "task_id": task_id,
            "completion": generate_one_completion(problems[task_id]["prompt"])
        }
    
    # List to hold future objects
    futures = []
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        for task_id in problems:
            for _ in range(num_samples_per_task):
                # Submit task to the thread pool
                future = executor.submit(generate_task_samples, task_id)
                futures.append(future)
                time.sleep(0.001) # To avoid same time calls
                time.sleep(delay_between_requests)  # Sleep to adhere to rate limit

    # Collecting results
    samples = [future.result() for future in as_completed(futures)]
    log.info("Generated %s samples", len(samples))
    return samples

if __name__ == "__main__":
    initialize_logging()

    optimal_number_of_threads = calculate_optimal_threads()
    problems = read_problems()
    samples = generate_answer_samples(problems, num_samples_per_task=1, max_threads=optimal_number_of_threads, requests_per_minute=3500)
    write_jsonl("samples.jsonl", samples)
