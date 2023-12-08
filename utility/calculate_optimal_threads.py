import multiprocessing
import logging as log


def calculate_optimal_threads(factor=5):
    """
    Calculate the optimal number of threads for I/O-bound tasks using thread pools.

    Args:
    - factor (int): A multiplier to apply to the number of CPU cores. The default value of 5 is a heuristic
                    for I/O-bound tasks, adjust based on empirical observations.

    Returns:
    - int: The calculated optimal number of threads.
    """
    num_cpu_cores = multiprocessing.cpu_count()
    optimal_threads = num_cpu_cores * factor
    log.info("Optimal number of threads: %s", optimal_threads)
    return optimal_threads


if __name__ == "__main__":
    # Example usage
    optimal_threads = calculate_optimal_threads()
    print(f"Optimal number of threads: {optimal_threads}")
