




test = ['assert min_cost([[1, 2, 3], [4, 8, 2], [1, 5, 3]], 2, 2) == 8', 'assert min_cost([[2, 3, 4], [5, 9, 3], [2, 6, 4]], 2, 2) == 12', 'assert min_cost([[3, 4, 5], [6, 10, 4], [3, 7, 5]], 2, 2) == 16']


import sys

def run_tests():
    exec(generated_code, globals())
    for t in test:
        exec(t, globals())

if __name__ == "__main__":
    run_tests()

