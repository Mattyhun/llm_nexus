from human_eval.data import write_jsonl, read_problems
from human_eval.evaluation import evaluate_functional_correctness
from gpt_api import generate_one_completion

problems = read_problems()

num_samples_per_task = 1
samples = [
    dict(task_id=task_id, completion=generate_one_completion(problems[task_id]["prompt"]))
    for task_id in problems
    for _ in range(num_samples_per_task)
]

if __name__ == "__main__":
    # write_jsonl("samples.jsonl", samples)

    for task_id in problems:
        print(problems[task_id]['prompt'])
        # print(problems[task_id]['test'])
        # print(problems[problem])
        print()

