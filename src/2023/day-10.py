from collections import namedtuple
import sys
import textwrap
import unittest

def run():
    with open("./input/2023-d10-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    pipes, start = read_pipes(input_data)
    path = walk(pipes, start)
    print("** Part 1 Final: ", depth(path))
    print("** Part 2 Final: ", 0)

def read_pipes(input_data):
    pipes = {}
    for r in range(len(input_data)):
        chars = list(input_data[r])
        for c in range(len(chars)):
            pipes[(r, c)] = chars[c]
            if chars[c] == 'S':
                start = (r, c)
    return (pipes, start)

def walk(pipes, start):
    stack = [(start, [])]
    while stack:
        node, visited = stack.pop()
        visited.append(node)
        neighbors = find_neighbors(pipes, node)
        # print(node, pipes.get(node), neighbors, " :: ", visited)
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append((neighbor, visited))
            if len(visited) > 2 and neighbor == start:
                print("Found a loop")
                return visited
    return []

#  | is a vertical pipe connecting north and south.
#  - is a horizontal pipe connecting east and west.
#  L is a 90-degree bend connecting north and east.
#  J is a 90-degree bend connecting north and west.
#  7 is a 90-degree bend connecting south and west.
#  F is a 90-degree bend connecting south and east.
#  . is ground; there is no pipe in this tile.
#  S is the starting position of the animal

def hasNorth(c):
    return c == 'S' or c == '|' or c == 'L' or c == 'J'
def hasSouth(c):
    return c == 'S' or c == '|' or c == '7' or c == 'F'
def hasEast(c):
    return c == 'S' or c == '-' or c == 'L' or c == 'F'
def hasWest(c):
    return c == 'S' or c == '-' or c == '7' or c == 'J'

def find_neighbors(pipes, node):
    current = pipes.get(node)
    neighbors = []
    if current == '.':
        return neighbors

    north = (node[0] - 1, node[1])
    south = (node[0] + 1, node[1])
    east = (node[0], node[1] + 1)
    west = (node[0], node[1] - 1)

    if hasNorth(current) and hasSouth(pipes.get(north)):
        neighbors.append(north)
    if hasSouth(current) and hasNorth(pipes.get(south)):
        neighbors.append(south)
    if hasEast(current) and hasWest(pipes.get(east)):
        neighbors.append(east)
    if hasWest(current) and hasEast(pipes.get(west)):
        neighbors.append(west)

    return neighbors

def depth(path):
    length = len(path)
    if length % 2 != 0:
        length += 1
    return length // 2

class TestSolution(unittest.TestCase):
    def test(self):
        # square loop
        input_data = textwrap.dedent("""
        -L|F7
        7S-7|
        L|7||
        -L-J|
        L|-JF
        """).split('\n')[1:-1]
        pipes, start = read_pipes(input_data)
        path = walk(pipes, start)
        self.assertEqual(depth(path), 4)

        print("------")
        input_data = textwrap.dedent("""
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
        """).split('\n')[1:-1]
        pipes, start = read_pipes(input_data)
        path = walk(pipes, start)
        self.assertEqual(depth(path), 8)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()