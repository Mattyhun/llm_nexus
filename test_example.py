import ast

# Function to extract function names from code
def extract_function_names(code):
    class FunctionNameExtractor(ast.NodeVisitor):
        def __init__(self):
            self.names = []

        def visit_FunctionDef(self, node):
            self.names.append(node.name)
            self.generic_visit(node)

    tree = ast.parse(code)
    extractor = FunctionNameExtractor()
    extractor.visit(tree)
    return extractor.names

# Function to run tests
def run_tests(code, tests, extracted_function_name):
    # Modify the tests to use the extracted function name
    modified_tests = [test.replace('min_cost', extracted_function_name) for test in tests]

    # Execute the code
    exec(code, globals())

    # Run each test
    for test in modified_tests:
        try:
            exec(test, globals())
            print(f"Test Passed: {test}")
        except AssertionError:
            print(f"Test Failed: {test}")

# Example usage
generated_code = """
def min_cost(cost, m, n):
    tc = [[0 for x in range(n+1)] for x in range(m+1)] 
    tc[0][0] = cost[0][0] 

    # Initialize first column of total cost(tc) array
    for i in range(1, m+1): 
        tc[i][0] = tc[i-1][0] + cost[i][0] 

    # Initialize first row of tc array
    for j in range(1, n+1): 
        tc[0][j] = tc[0][j-1] + cost[0][j] 

    for i in range(1, m+1): 
        for j in range(1, n+1): 
            tc[i][j] = min(tc[i-1][j-1], tc[i-1][j], tc[i][j-1]) + cost[i][j]     

    return tc[m][n]
"""

test_cases = [
    'assert min_cost([[1, 2, 3], [4, 8, 2], [1, 5, 3]], 2, 2) == 8',
    'assert min_cost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) == 12',
    'assert min_cost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) == 16'
]

# Extract function names from the generated code
function_names = extract_function_names(generated_code)

# Assuming the first function name is the one we want to test
if function_names:
    run_tests(generated_code, test_cases, function_names[0])
else:
    print("No function found in the generated code.")
