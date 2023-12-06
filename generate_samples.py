from concurrent.futures import ThreadPoolExecutor, as_completed
from utility.calculate_optimal_threads import calculate_optimal_threads
from human_eval.data import write_jsonl, read_problems
from generate_one_completion import generate_one_completion
import logging as log
from project_config import initialize_logging
import time
from tqdm import tqdm  # Import tqdm for the progress bar

def generate_answer_samples(model, problems, num_samples_per_task=1, max_threads=50, requests_per_minute=3500):
    # Calculate delay between requests to adhere to the rate limit
    delay_between_requests = 60 / requests_per_minute  # in seconds

    # Function to generate samples for a single task
    def generate_task_samples(task_id):
        log.debug("Generating samples for task %s", task_id)
        return {
            "task_id": task_id,
            "completion": generate_one_completion(model, problems[task_id]["prompt"])
        }
    
    # Total number of tasks
    total_tasks = len(problems) * num_samples_per_task

    # List to hold future objects and results
    futures = []
    samples = []

    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Initialize progress bar
        with tqdm(total=total_tasks, desc="Generating Samples") as progress_bar:
            for task_id in problems:
                for _ in range(num_samples_per_task):
                    # Submit task to the thread pool
                    future = executor.submit(generate_task_samples, task_id)
                    futures.append(future)
                    time.sleep(0.001)  # To avoid same time calls
                    time.sleep(delay_between_requests)  # Sleep to adhere to rate limit

            # Collecting results and updating progress bar
            for future in as_completed(futures):
                result = future.result()  # Wait for the future to complete if it hasn't yet
                samples.append(result)
                progress_bar.update(1)  # Update the progress bar by one step

    log.info("Generated %s samples", len(samples))
    return samples

if __name__ == "__main__":
    initialize_logging()

    optimal_number_of_threads = calculate_optimal_threads()
    problems = read_problems()
    samples = generate_answer_samples('gpt-3.5-turbo', problems, num_samples_per_task=1, max_threads=optimal_number_of_threads, requests_per_minute=3500)
    write_jsonl("samples.jsonl", samples)
