import matplotlib.path as mplPath
import networkx as nx
import sys
import textwrap
import unittest

def run():
    with open("./input/2023-d10-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    pipes = plot_pipes(input_data)
    g, s = pipes_to_graph(pipes)
    path = find_cycle_from_start(g, s)
    print("** Part 1 Final: ", max_depth(path))

    print("** Part 2 Final: ", 0)

#  | is a vertical pipe connecting north and south.
#  - is a horizontal pipe connecting east and west.
#  L is a 90-degree bend connecting north and east.
#  J is a 90-degree bend connecting north and west.
#  7 is a 90-degree bend connecting south and west.
#  F is a 90-degree bend connecting south and east.
#  . is ground; there is no pipe in this tile.
#  S is the starting position of the animal

def plot_pipes(input_data):
    # plot the pipes in a 2D array
    # return the array
    pipes = []
    for line in input_data:
        pipes.append(list(line))
    return pipes

def pipes_to_graph(pipes):
    G = nx.DiGraph()
    start = None
    max_i = len(pipes)
    max_j = len(pipes[0])
    for i in range(len(pipes)):
        for j in range(len(pipes[i])):
            if pipes[i][j] == '.':
                continue
            G.add_node((i, j), key=pipes[i][j])
            if pipes[i][j] == 'S':
                start = (i, j)
            elif pipes[i][j] == '|': # vertical
                add_edge(G, pipes, max_i, max_j, (i, j), (i-1, j), (i+1, j))
            elif pipes[i][j] == '-': # horizontal
                add_edge(G, pipes, max_i, max_j, (i, j), (i, j-1), (i, j+1))
            elif pipes[i][j] == 'L': # north-to-east
                add_edge(G, pipes, max_i, max_j, (i, j), (i-1, j), (i, j+1))
            elif pipes[i][j] == 'J': # north-to-west
                add_edge(G, pipes, max_i, max_j, (i, j), (i-1, j), (i, j-1))
            elif pipes[i][j] == '7': # south-to-west
                add_edge(G, pipes, max_i, max_j, (i, j), (i+1, j), (i, j-1))
            elif pipes[i][j] == 'F': # south-to-east
                add_edge(G, pipes, max_i, max_j, (i, j), (i+1, j), (i, j+1))

    # Treat all edges into the start as bidirectional
    for edge in G.in_edges(start):
        G.add_edge(edge[1], edge[0])

    return G, start

def add_edge(G, pipes, max_i, max_j, node, *neighbors):
    for neighbor in neighbors:
        i, j = neighbor
        if 0 <= i < max_i and 0 <= j < max_j and pipes[i][j] != '.':
            G.add_edge(node, neighbor)  # Add a directed edge

def find_cycle_from_start(G, start):
    cycles = list(nx.simple_cycles(G))
    cycles = [cycle for cycle in cycles if start in cycle and len(cycle) > 2]

    normalized_cycles = []
    for cycle in cycles:
        min_index = cycle.index(start)
        normalized_cycle = cycle[min_index:] + cycle[:min_index]
        normalized_cycles.append(normalized_cycle)

    if (len(normalized_cycles) > 2):
        print("Found multiple cycles:")
        print(normalized_cycles)
    elif (len(normalized_cycles) == 2):
        if set(normalized_cycles[0]) == set(normalized_cycles[1]):
            normalized_cycles.pop(1)
        else:
            print("Found multiple cycles:")
            print(normalized_cycles)

    return normalized_cycles[0]

def max_depth(path):
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
        pipes = plot_pipes(input_data)
        g, s = pipes_to_graph(pipes)
        path = find_cycle_from_start(g, s)
        self.assertEqual(max_depth(path), 4)

        print("------")
        input_data = textwrap.dedent("""
        7-F7-
        .FJ|7
        SJLL7
        |F--J
        LJ.LJ
        """).split('\n')[1:-1]
        pipes = plot_pipes(input_data)
        g, s = pipes_to_graph(pipes)
        path = find_cycle_from_start(g, s)
        self.assertEqual(max_depth(path), 8)


if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()