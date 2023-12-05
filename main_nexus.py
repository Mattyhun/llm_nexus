


select_model()

select_problem()

send_query_to_model()

send_tests_to_vm()

await_llm_code_result()

send_code_result_to_testing_vm()

initiate_testing_on_vm()

testing_result = await_testing_result()


while testing_result == "failed":
    send_test_result_back_to_model()

send_code_result_to_evaluator()

evaluator_result = await_evaluator_result()

