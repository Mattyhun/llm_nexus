import json
import os
from generate_samples import generate_answer_samples
from human_eval.data import read_problems, write_jsonl
from vm_communication import run_command_on_vm, transfer_file_to_vm, validate_file_path



# select_model()

# select_problem()

# send_query_to_model()
problems = read_problems()
samples = generate_answer_samples(problems)
write_jsonl("samples11.jsonl", samples)   

# await_llm_code_result()

# send_tests_to_vm()
# send_code_result_to_testing_vm()
transfer_file_to_vm("samples11.jsonl", "samples11.jsonl")

# initiate_testing_on_vm()
testing_result = run_command_on_vm("python3 human-eval/human_eval/evaluate_functional_correctness.py samples11.jsonl")

print(testing_result)

# # optional
# # while testing_result == "failed":
# #     send_test_result_back_to_model()

# send_code_result_to_evaluator()

# evaluator_result = await_evaluator_result()

