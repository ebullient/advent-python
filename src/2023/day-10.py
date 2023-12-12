from collections import namedtuple
import sys
import textwrap
import unittest

def run():
    with open("./input/2023-d10-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    pipes, start = read_pipes(input_data)
    path = walk(pipes, start)
    enclosed = scan(pipes, path, len(input_data), len(input_data[0]))
    print("** Part 1 Final: ", depth(path))
    print("** Part 2 Final: ", enclosed)

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
                return visited
    print(pipes)
    return []

def scan(pipes, path, rows, cols):
    enclosed = 0;
    for r in range(rows):
        inside = False
        for c in range(cols):
            pixel = pipes.get((r, c))
            in_path = (r, c) in path
            if in_path:
                if pixel == 'F' or pixel == '7' or pixel == '|':
                    inside = not inside
            elif inside:
                enclosed += 1
                pixel = 'I'
            else:
                pixel = 'O'
            print(draw(pixel), end='')
        print()
    return enclosed

def draw(x):
    if x == 'S':
        return 'S'
    if x == '|':
        return '│'
    if x == '-':
        return '─'
    if x == 'F':
        return '┌'
    if x == '7':
        return '┐'
    if x == 'L':
        return '└'
    if x == 'J':
        return '┘'
    return x

#  | is a vertical pipe connecting north and south.
#  - is a horizontal pipe connecting east and west.
#  L is a 90-degree bend connecting north and east.
#  J is a 90-degree bend connecting north and west.
#  7 is a 90-degree bend connecting south and west.
#  F is a 90-degree bend connecting south and east.
#  . is ground; there is no pipe in this tile.
#  S is the starting position of the animal

def hasNorth(c):
    return c == '|' or c == 'L' or c == 'J'
def hasSouth(c):
    return c == '|' or c == '7' or c == 'F'
def hasEast(c):
    return c == '-' or c == 'L' or c == 'F'
def hasWest(c):
    return c == '-' or c == '7' or c == 'J'

def find_neighbors(pipes, node):
    current = pipes.get(node)
    neighbors = []
    if current == '.':
        return neighbors

    north = (node[0] - 1, node[1])
    south = (node[0] + 1, node[1])
    east = (node[0], node[1] + 1)
    west = (node[0], node[1] - 1)

    if current == 'S':
        if hasNorth(pipes.get(south)) and hasSouth(pipes.get(north)):
            current = '|'
        elif hasEast(pipes.get(west)) and hasWest(pipes.get(east)):
            current = '-'
        elif hasNorth(pipes.get(south)) and hasEast(pipes.get(west)):
            current = '7'
        elif hasNorth(pipes.get(south)) and hasWest(pipes.get(east)):
            current = 'F'
        elif hasSouth(pipes.get(north)) and hasEast(pipes.get(west)):
            current = 'J'
        elif hasSouth(pipes.get(north)) and hasWest(pipes.get(east)):
            current = 'L'
        pipes[node] = current

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
        enclosed = scan(pipes, path, len(input_data), len(input_data[0]))
        self.assertEqual(enclosed, 1)

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
        scan(pipes, path, len(input_data), len(input_data[0]))


        print("------")
        input_data = textwrap.dedent("""
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
        """).split('\n')[1:-1]

        pipes, start = read_pipes(input_data)
        path = walk(pipes, start)
        enclosed = scan(pipes, path, len(input_data), len(input_data[0]))
        self.assertEqual(enclosed, 8)

        print("------")
        input_data = textwrap.dedent("""
        FF7FSF7F7F7F7F7F---7
        L|LJ||||||||||||F--J
        FL-7LJLJ||||||LJL-77
        F--JF--7||LJLJ7F7FJ-
        L---JF-JLJ.||-FJLJJ7
        |F|F-JF---7F7-L7L|7|
        |FFJF7L7F-JF7|JL---7
        7-L-JL7||F7|L7F-7F7|
        L.L7LFJ|||||FJL7||LJ
        L7JLJL-JLJLJL--JLJ.L
        """).split('\n')[1:-1]

        pipes, start = read_pipes(input_data)
        path = walk(pipes, start)
        enclosed = scan(pipes, path, len(input_data), len(input_data[0]))
        self.assertEqual(enclosed, 10)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()