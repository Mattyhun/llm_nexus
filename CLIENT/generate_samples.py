from concurrent.futures import ThreadPoolExecutor, as_completed
import logging as log
import time
from tqdm import tqdm  # Import tqdm for the progress bar
from project_config import initialize_logging
from generate_one_completion import generate_one_completion
from utility.data_handler import write_jsonl, read_problems
from utility.calculate_optimal_threads import calculate_optimal_threads

def generate_answer_samples(interface, model, problems, num_samples_per_task=1, max_threads=50, requests_per_minute=3500):
    """
    Generate samples of model's answers for given tasks/problems.

    This function uses a thread pool to concurrently generate multiple
    samples. It respects the rate limit by introducing a delay between each 
    request. The function also updates a progress bar as it works its way
    through the tasks.

    Parameters:
    - model: The language model to use.
    - problems: Dictionary with task/problem ids as keys and corresponding 
        prompts as values.
    - num_samples_per_task (optional): Number of samples to generate per task/problem.
        Default is 1.
    - max_threads (optional): Maximum number of threads to be used in the thread pool.
        Default is 50.
    - requests_per_minute (optional): The rate limit for making requests to the API.
        Default is 3500.

    Returns:
    - A list of dictionaries, where each dictionary contains the 'task_id' and the 
      'completion' i.e., the generated answer for the task.
    """

    # Calculate delay between requests to adhere to the rate limit
    delay_between_requests = 60 / requests_per_minute  # in seconds

    def generate_task_samples(task_id):
        '''
        Function to generate samples for a single task
        returns a dictionary with the task_id and the completion
        '''
        log.debug("Generating samples for task %s", task_id)
        return {
            "task_id": task_id,
            "completion": generate_one_completion(interface, model, problems[task_id]["prompt"])
        }

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
                    # Sleep to adhere to rate limit
                    time.sleep(delay_between_requests)

            # Collecting results and updating progress bar
            for future in as_completed(futures):
                result = future.result()  # Wait for the future to complete if it hasn't yet
                samples.append(result)
                progress_bar.update(1)  # Update the progress bar by one step

    log.info("Generated %s samples", len(samples))
    return samples


if __name__ == "__main__":
    initialize_logging()
    model = "gpt-3.5-turbo"
    optimal_number_of_threads = calculate_optimal_threads()
    problems = read_problems()
    samples = generate_answer_samples(model, problems, num_samples_per_task=1,
                                      max_threads=optimal_number_of_threads, requests_per_minute=3500)
    write_jsonl("samples.jsonl", samples)
