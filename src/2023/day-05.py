from collections import namedtuple
from intervaltree import Interval, IntervalTree
import sys
import textwrap
import unittest

Data = namedtuple('Data', ['dest', 'range'])

def run():
    with open("./input/2023-d05-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    maps = parse_map(input_data)
    seeds = maps.get('seeds')

    locations = []
    for seed in seeds:
        locations.append(seed_to_location(maps, seed))
    print("** Part 1 Final: ", min(locations))

    locations = []
    for i in range(0, len(seeds), 2):
        locations.extend(seed_range_to_locations(maps, seeds[i], seeds[i+1]))
    print("Hops: ", maps['hops'])

    print("** Part 2 Final: ", min(locations))

def parse_map(input_data):
    input_data.append('') # add an empty line to the end of the input data
    maps = {}
    heading = ''
    t = IntervalTree()
    for line in input_data:
        if line.startswith('seeds:'):
            seeds = [int(x) for x in line.split(':')[1].strip().split()]
            maps['seeds'] = seeds
        elif line == '':
            if (heading != ''):
                maps[heading] = t
                t = IntervalTree()
                heading = ''
            continue
        elif line.endswith('map:'):
            heading = line.replace(' map:', '').strip()
            continue
        else:
            [dest, start, range] = [int(x) for x in line.split()]
            t.add(Interval(start, start+range, Data(dest, range)))
    return maps

def seed_range_to_locations(maps, begin, range):
    sequence = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    locations = []
    maps['hops'] = 0
    check_range(maps, sequence, 0, locations, begin, begin+range)
    return locations

def check_range(maps, sequence, s, locations, begin, end):
    maps['hops'] += 1
    if (s >= len(sequence)):
        locations.append(begin)
        return
    key = sequence[s]
    tree = maps.get(key)
    ranges = tree[begin:end]
    leftover = []
    if ranges:
        for item in ranges:
            delta = item.data.dest - item.begin
            if item.begin <= begin and end <= item.end:
                # completely enveloped range
                check_range(maps, sequence, s + 1, locations, begin + delta, end + delta)
                return
            elif item.begin <= begin:
                # partially overlapping range
                check_range(maps, sequence, s + 1, locations, begin + delta, item.end + delta)
                leftover.append((item.end, end))
            elif item.end >= end:
                # partially overlapping range
                check_range(maps, sequence, s + 1, locations, item.begin + delta, end + delta)
                leftover.append((begin, item.begin))
    else:
        check_range(maps, sequence, s + 1, locations, begin, end)

    ## Sloppy, but it works.
    for (begin, end) in leftover:
        check_range(maps, sequence, s, locations, begin, end)

def seed_to_location(maps, seed):
    sequence = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light', 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    i = seed
    for key in sequence:
        tree = maps.get(key)
        if tree and tree[i]:
            for item in tree[i]:
                data = item.data
                i = data.dest + (i - item.begin)

    return i

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines


        maps = parse_map(input_data)
        # Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
        self.assertEqual(seed_to_location(maps, 79), 82)
        # Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
        self.assertEqual(seed_to_location(maps, 14), 43)
        # Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
        self.assertEqual(seed_to_location(maps, 55), 86)
        # Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
        self.assertEqual(seed_to_location(maps, 13), 35)


        locations = seed_range_to_locations(maps, 79, 14)
        self.assertEqual(min(locations), 46)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()