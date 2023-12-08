from collections import namedtuple
from functools import reduce
import math
import sys
import textwrap
import unittest

MapData = namedtuple('MapData', ['instructions', 'network'])
Node = namedtuple('Node', ['name', 'L', 'R'])
all_z = lambda x: x.name == 'ZZZ'
end_z = lambda x: x.name.endswith('Z')

def run():
    with open("./input/2023-d08-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    desert_map = create_map(input_data)
    print("** Part 1 Final: ", walk(desert_map, desert_map.network['AAA'], 0, all_z))
    print("** Part 2 Final: ", ghost_walk(desert_map))

def create_map(input_data):
    instructions = list(input_data.pop(0))
    input_data.pop(0) # empty line
    nodes = {}
    for line in input_data:
        node, edges = line.split(' = ')
        edges = edges.replace('(', '').replace(')', '').split(', ')
        nodes[node] = Node(node, edges[0], edges[1])

    return MapData(instructions, nodes)

# Part 1
# Starting with AAA, you need to look up the next element
# based on the next left/right instruction in your input.
# If you run out of left/right instructions, repeat the whole sequence of instructions as necessary
# Part 2
# the number of nodes with names ending in A is equal to the number ending in Z!
# start at every node that ends with A and follow all of the paths at the same time

def ghost_walk(map):
    a_nodes = [x for x in map.network.values() if x.name.endswith('A')]
    scores = [(x, walk(map, x, 0, end_z)) for x in a_nodes]
    return lcm_multiple([x[1] for x in scores])

# THE TOOOOOO LLLOOOOOOONNNNGGGG WAY
# def ghost_walk(map, start_nodes):
#     i = 0
#     nodes = start_nodes
#     while True:
#        for instruction in map.instructions:
#            next_nodes = []
#            i += 1
#            if instruction == 'L':
#                next_nodes = [map.network.get(x.L) for x in nodes]
#            elif instruction == 'R':
#                next_nodes = [map.network.get(x.R) for x in nodes]
#            if all(x.name.endswith('Z') for x in next_nodes):
#                return (i, next_nodes)
#            nodes = next_nodes

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def lcm_multiple(numbers):
    return reduce(lcm, numbers)

def walk(map, start_node, i, fn):
    node = start_node
    while True:
        for instruction in map.instructions:
            next = None
            i += 1
            if instruction == 'L':
                next = map.network.get(node.L)
            else:
                next = map.network.get(node.R)
            if fn(next):
                return i
            node = next

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
        RL

        AAA = (BBB, CCC)
        BBB = (DDD, EEE)
        CCC = (ZZZ, GGG)
        DDD = (DDD, DDD)
        EEE = (EEE, EEE)
        GGG = (GGG, GGG)
        ZZZ = (ZZZ, ZZZ)
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        desert_map = create_map(input_data)
        self.assertEqual(walk(desert_map, desert_map.network['AAA'], 0, all_z), 2)

        input_data = textwrap.dedent("""
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        desert_map = create_map(input_data)
        self.assertEqual(walk(desert_map, desert_map.network['AAA'], 0, all_z), 6)

        ## Part 2
        input_data = textwrap.dedent("""
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        desert_map = create_map(input_data)
        self.assertEqual(ghost_walk(desert_map), 6)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()