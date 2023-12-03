test = ['assert min_cost([[1, 2, 3], [4, 8, 2], [1, 5, 3]], 2, 2) == 8', 'assert min_cost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) == 12', 'assert min_cost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) == 16']
import re

# Extract the function name from the generated_code
generated_function_name = re.search(r'def (\w+)\(', generated_code).group(1)

# Extract the function name from the first test
test_function_name = re.search(r'assert (\w+)\(', test[0]).group(1)

# Replace the function name in generated_code
generated_code = generated_code.replace(generated_function_name, test_function_name)

# Replace the function name in generated_code
generated_code = generated_code.replace('generated_function_name', function_name)

import sys

def run_tests():
    exec(generated_code, globals())
    for t in test:
        exec(t, globals())

if __name__ == "__main__":
    run_tests()

