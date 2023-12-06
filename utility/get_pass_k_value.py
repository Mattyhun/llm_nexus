import re

def get_pass_k_value(output_text):
    # Search for the pattern "pass@k": followed by a floating point number
    match = re.search(r"'pass@(\d+)': (\d+\.\d+)", output_text)
    
    # If a match is found, return the pass@k value
    if match:
        k_value = match.group(1)
        pass_value = float(match.group(2))
        return f"pass@{k_value}: {pass_value}"
    else:
        return "pass@k value not found"

if __name__ == '__main__':
    # Example usage
    output_text = """
    Reading samples...
    0it [00:00, ?it/s]Running test suites...
    164it [00:00, 9115.51it/s]
    100%|██████████| 164/164 [00:02<00:00, 67.68it/s]
    Writing results to samples.jsonl_results.jsonl...
    100%|██████████| 164/164 [00:00<00:00, 75739.47it/s]
    {'pass@1': 0.3170731707317073}
    """

    print(get_pass_k_value(output_text))