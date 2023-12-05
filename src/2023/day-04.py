from collections import namedtuple
import sys
import textwrap
import unittest

class CardCounter:
    def __init__(self, count, num_winners):
        self.count = count
        self.num_winners = num_winners
    def __str__(self):
        return f'CardCounter(count={self.count}, num_winners={self.num_winners})'

def run():
    with open("./input/2023-d04-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    result = 0
    card_data = read_cards(input_data)

    ## Part 1
    for card in card_data:
        result += score(winning_numbers(card))

    ## Part 2
    cards = find_winning_cards(card_data)

    print("** Part 1 Final: ", result)
    print("** Part 2 Final: ", total(cards))

# card has two lists of numbers separated by a vertical bar (|):
#   a list of winning numbers and then a list of numbers you have
# figure out which of the numbers you have appear in the list of winning numbers:
# - the first match makes the card worth one point
# - each match after the first doubles the point value of that card.

def read_cards(input_data):
    cards = []
    for line in input_data:
        cards.append(line.split(':')[1].strip())
    return cards

def find_winning_cards(card_data):
    card_map = []
    for i, card in enumerate(card_data):
        winners = winning_numbers(card)
        card_map.append(CardCounter(1, len(winners)))

    for i, card in enumerate(card_map):
        if card.num_winners > 0:
            for j in range(i+1, i+card.num_winners+1):
                card_map[j].count += card.count
    return card_map

def winning_numbers(card):
    parts = card.split('|')
    winning_numbers = parts[0].split() # split on whitespace
    numbers = parts[1].split() # split on whitespace
    return list(filter(lambda x: x in winning_numbers, numbers))

def total(cards):
    return sum(CardCounter.count for CardCounter in cards)

def score(numbers):
    return 2 ** (len(numbers) - 1) if numbers else 0

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
        Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
        Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
        Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
        Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
        Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
        Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        card_data = read_cards(input_data)

        ## Part 1
        result = winning_numbers(card_data[0])
        self.assertListEqual(result, ['83', '86', '17', '48'])
        self.assertEqual(score(result), 8)

        result = winning_numbers(card_data[3])
        self.assertListEqual(result, ['84'])
        self.assertEqual(score(result), 1)

        result = winning_numbers(card_data[5])
        self.assertListEqual(result, [])
        self.assertEqual(score(result), 0)

        ## Part 2
        cards = find_winning_cards(card_data)
        self.assertEqual(total(cards), 30)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()