from collections import namedtuple
import re
import sys
import textwrap
import unittest

# Define the tuple type: red, green, blue cubes
CubeSet = namedtuple('CubeSet', ['red', 'green', 'blue'])

SPLICE = re.compile(r"Game (\d+): (.*)\s*")
CUBES = re.compile(r"(\d+) (\w+)")

def run():
    with open("./input/2023-d02-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    # Part 1:
    # which games would have been possible if the bag contained 
    # only 12 red cubes, 13 green cubes, and 14 blue cubes
    games = find_all_games(input_data)
    print("** Part 1 Final: ", find_possible_games(games, CubeSet(12, 13, 14)))
    print("** Part 2 Final: ", find_possible_games_power(games))

def find_all_games(input_data):
    games = {}
    for game_string in input_data:
        match = SPLICE.search(game_string)
        if match:
            games[match.group(1)] = parse_cubes(match.group(2))

    return games

def parse_cubes(grouped_cubesets):
    cubesets = []
    for cubeset in re.split(r'\s*;\s*', grouped_cubesets):
        red = 0
        green = 0
        blue = 0
        for cubes in re.split(r'\s*,\s*', cubeset):
            match = CUBES.search(cubes.strip())
            if match:
                if match.group(2) == 'red':
                    red += int(match.group(1))
                elif match.group(2) == 'green':
                    green += int(match.group(1))
                elif match.group(2) == 'blue':
                    blue += int(match.group(1))
                    
        cubesets.append(CubeSet(red, green, blue))

    return cubesets

def is_game_possible(game_cube_set, actual_cube_set):
    max_red = max(cubeset.red for cubeset in game_cube_set)
    max_green = max(cubeset.green for cubeset in game_cube_set)
    max_blue = max(cubeset.blue for cubeset in game_cube_set)

    return max_red <= actual_cube_set.red and \
        max_green <= actual_cube_set.green and \
        max_blue <= actual_cube_set.blue

def find_possible_games(games, actual_cube_set):
    possible_games = 0
    for game in games:
        if is_game_possible(games[game], actual_cube_set):
            possible_games += int(game)

    return possible_games

def game_power(game_cube_set):
    max_red = max(cubeset.red for cubeset in game_cube_set)
    max_green = max(cubeset.green for cubeset in game_cube_set)
    max_blue = max(cubeset.blue for cubeset in game_cube_set)

    return max_red * max_green * max_blue

def find_possible_games_power(games):
    power = 0
    for game in games:
        power += game_power(games[game])

    return power

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines
        
        games = find_all_games(input_data)
        self.assertEqual(find_possible_games(games, CubeSet(12, 13, 14)), 8)

        self.assertEqual(game_power(games['1']), 48)
        self.assertEqual(game_power(games['2']), 12)
        self.assertEqual(game_power(games['3']), 1560)
        self.assertEqual(game_power(games['4']), 630)
        self.assertEqual(game_power(games['5']), 36)

        self.assertEqual(find_possible_games_power(games), 2286)


if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()