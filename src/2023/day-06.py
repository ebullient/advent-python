from collections import namedtuple
import sys
import textwrap
import unittest

RaceRecord = namedtuple('RaceRecord', ['time', 'distance'])

def run():
    with open("./input/2023-d06-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    records = race_records(input_data)
    print("** Part 1 Final: ", find_optimal_button_press_time(records))

    records = race_records(input_data, True)
    print("** Part 2 Final: ", find_optimal_button_press_time(records))

## Boats move faster if their button was held longer, but time spent holding the button counts against the total race time.
## You can only hold the button at the start of the race, and boats don't move until the button is released.

# Your toy boat has a starting speed of zero millimeters per millisecond.
# For each whole millisecond you spend at the beginning of the race holding down the button,
# the boat's speed increases by one millimeter per millisecond.

def decode(input, strip):
    if strip:
        input = input.replace(' ', '')
    return input.split()

def race_records(input_data, strip=False):
    times = []
    distances = []
    records = []
    for line in input_data:
        if line.startswith('Time:'):
            times = [int(x) for x in decode(line.split(':')[1], strip)]
        elif line.startswith('Distance:'):
            distances = [int(x) for x in decode(line.split(':')[1], strip)]

    for i in range(len(times)):
        records.append(RaceRecord(times[i], distances[i]))
    return records

# product: optimal button press time
def find_optimal_button_press_time(records):
    ways_to_win = 1
    for record in records:
        ways_to_win *= winners_for_race(record)
    return ways_to_win

def winners_for_race(race):
    winners = 0
    for i in range(1, race.time):
        distance = button_to_distance(race.time, i)
        if distance > race.distance:
            winners += 1
    return winners

# total time (tt), button time (bt); return distance traveled
def button_to_distance(tt, bt):
    mt = tt - bt
    return bt * mt

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
        Time:      7  15   30
        Distance:  9  40  200
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        records = race_records(input_data)

        self.assertEqual(button_to_distance(records[0].time, 0), 0)
        self.assertEqual(button_to_distance(records[0].time, 1), 6)
        self.assertEqual(button_to_distance(records[0].time, 2), 10)
        self.assertEqual(button_to_distance(records[0].time, 3), 12)
        self.assertEqual(button_to_distance(records[0].time, 4), 12)
        self.assertEqual(button_to_distance(records[0].time, 5), 10)
        self.assertEqual(button_to_distance(records[0].time, 6), 6)
        self.assertEqual(button_to_distance(records[0].time, 7), 0)

        self.assertEqual(winners_for_race(records[0]), 4)
        self.assertEqual(winners_for_race(records[1]), 8)
        self.assertEqual(winners_for_race(records[2]), 9)

        self.assertEqual(find_optimal_button_press_time(records), 288)

        records = race_records(input_data, True)
        self.assertEqual(find_optimal_button_press_time(records), 71503)


if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()