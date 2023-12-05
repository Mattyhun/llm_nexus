import ast
import socket

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

def run_tests(code, tests, extracted_function_name):
    modified_tests = [test.replace('your_function', extracted_function_name) for test in tests]
    exec(code, globals())
    results = []
    for test in modified_tests:
        try:
            exec(test, globals())
            results.append(f"Test Passed: {test}")
        except AssertionError:
            results.append(f"Test Failed: {test}")
    return results

def server_program():
    host = '127.0.0.1'
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))

    server_socket.listen(2)
    conn, address = server_socket.accept()

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        # Hibakezelés a nem megfelelő formátumú adatok esetén
        if '####' in data:
            code, tests = data.split('####')
            tests = tests.split(';')
            function_names = extract_function_names(code)
            if function_names:
                results = run_tests(code, tests, function_names[0])
                conn.send(';'.join(results).encode())
            else:
                conn.send("Nem található funkció a kódban.".encode())
        else:
            conn.send("Hibás adatformátum.".encode())

    conn.close()

if __name__ == '__main__':
    server_program()
