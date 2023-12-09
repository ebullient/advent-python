import numpy as np
import sys
import textwrap
import unittest

def run():
    with open("./input/2023-d09-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    history = full_history(input_data)
    print(history)
    print("** Part 1 Final: ", extrapolate_all(history))
    print("** Part 2 Final: ", extrapolate_all(history, True))

def full_history(input_data):
    history = []
    for line in input_data:
        history.append([int(x) for x in line.split(' ')])
    return history

def extrapolate_all(history, reverse=False):
    result = 0
    for line in history:
        result += extrapolate(line, reverse)
    return result

def extrapolate(history, reverse=False):
    diff = [history]
    while len(diff[-1]) > 1:
        next = np.diff(diff[-1]).tolist()
        if all(x == 0 for x in next):
            break
        diff.append(next)
    for i in range(len(diff)-2, -1, -1):
        if reverse:
            diff[i].insert(0, diff[i][0] - diff[i+1][0])
        else:
            diff[i].append(diff[i][-1] + diff[i+1][-1])
    if reverse:
        return diff[0][0]
    return diff[0][-1]

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
        0 3 6 9 12 15
        1 3 6 10 15 21
        10 13 16 21 30 45
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        history = full_history(input_data)
        self.assertEqual(extrapolate_all(history), 114)
        self.assertEqual(extrapolate_all(history, True), 2)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()