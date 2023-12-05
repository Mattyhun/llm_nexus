from datasets import load_dataset

dataset = load_dataset("mbpp")

def get_prompt_from_id(task_id, dataset):
    for entry in dataset:
        # Check if the entry is a dictionary and has a 'task_id' key
        if isinstance(entry, dict) and 'task_id' in entry:
            if entry['task_id'] == task_id:
                return entry.get('text', "Text not found.")
    return "Task ID not found."


def get_test_dataset():
    # Load the dataset
    dataset = load_dataset("mbpp")
    # Return the test subset of the dataset
    return dataset['test']

# Example usage


if __name__ == "__main__":
    test_dataset = get_test_dataset()

    print(test_dataset)
    print(get_prompt_from_id(12, test_dataset))