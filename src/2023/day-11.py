from itertools import combinations
import sys
import textwrap
import unittest

def run():
    with open("./input/2023-d11-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    result = scan(input_data)
    galaxies = expand(result, 1)
    print("** Part 1 Final: ", shortest_paths(galaxies))

    galaxies = expand(result, 1000000-1) #lazy
    print("** Part 2 Final: ", shortest_paths(galaxies))

def scan(input_data):
    empty_rows = list(range(len(input_data)))
    empty_cols = list(range(len(input_data[0])))
    g = {}
    label = 1
    for row in range(len(input_data)):
        for col in range(len(input_data[0])):
            if input_data[row][col] == '#':
                tryRemove(empty_rows, row)
                tryRemove(empty_cols, col)
                g[(row, col)] = (label, (row, col))
                label += 1

    return (g, empty_rows, empty_cols)

def expand(x, factor):
    g = x[0]
    empty_rows = x[1]
    empty_cols = x[2]
    galaxies = {}
    for key, value in g.items():
        coord_row = value[1][0]
        coord_col = value[1][1]
        for r in empty_rows:
            if key[0] > r:
                coord_row += factor

        for c in empty_cols:
            if key[1] > c:
                coord_col += factor

        galaxies[value[0]] = (coord_row, coord_col)
    return galaxies

def shortest_paths(galaxies):
    result = 0
    for g1, g2 in combinations(galaxies.values(), 2):
        result += md(g1, g2)
    return result

def tryRemove(list, x):
    try:
        list.remove(x)
    except ValueError:
        pass

def md(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def show(result, galaxies):
    for k, v in result[0].items():
        print(v[0], v[1], ' -> ', galaxies[v[0]])

class TestSolution(unittest.TestCase):
    def test(self):

        input_data = textwrap.dedent("""
        ...#......
        .......#..
        #.........
        ..........
        ......#...
        .#........
        .........#
        ..........
        .......#..
        #...#.....
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        result = scan(input_data)
        galaxies = expand(result, 1)
        self.assertEqual(md(galaxies[1], galaxies[7]), 15)
        self.assertEqual(md(galaxies[3], galaxies[6]), 17)
        self.assertEqual(md(galaxies[8], galaxies[9]), 5)
        self.assertEqual(shortest_paths(galaxies), 374)

        galaxies = expand(result, 9)
        self.assertEqual(shortest_paths(galaxies), 1030)
        galaxies = expand(result, 99)
        self.assertEqual(shortest_paths(galaxies), 8410)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()