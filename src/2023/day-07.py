from collections import namedtuple
from enum import Enum
from itertools import groupby
from operator import attrgetter
import sys
import textwrap
import unittest

# In Camel Cards, players arrange hands of cards by strength.
# Each hand has five cards labeled A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2, with A being the highest and 2 the lowest.

class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

Hand = namedtuple('Hand', ['cards', 'type', 'bid'])

def run():
    with open("./input/2023-d07-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    hands = get_hands(input_data)
    ranked_hands = rank_hands(hands)
    print("** Part 1 Final: ", total_winnings(ranked_hands))

    hands = get_hands(input_data, True)
    ranked_hands = rank_hands(hands, True)
    print("** Part 2 Final: ", total_winnings(ranked_hands))

# Hands are ranked by type, then by individual card strength if hands are of the same type.
# For same-type hands, compare cards in order: the hand with the stronger first card wins,
# or move to the next card if the first cards match, and so on.
#
# Input: Hand of cards, bid
# Rank hands from weakest (1) to strongest (n)
# Total winnings: add up the result of bid*rank for each hand

def get_hands(input_data, joker=False):
    hands = []
    for line in input_data:
        hand, bid = line.split(' ')
        if joker:
            type = classify_hand_joker(hand)
        else:
            type = classify_hand(hand)
        hands.append(Hand(hand, type, int(bid)))
    return hands

# Five of a kind: All cards have the same label 1.
# Four of a kind: Four cards of the same label 1, one different 2.
# Full house: Three cards of one label 1, two of another 2.
# Three of a kind: Three cards of one label 1, two different cards 23.
# Two pair: Two sets of pairs 12, one different card 3.
# One pair: One pair 1, three different cards 234.
# High card: All cards have different labels 12345.

JOKER_UPGRADES = {
    (3, HandType.FULL_HOUSE): HandType.FIVE_OF_A_KIND,
    (2, HandType.FULL_HOUSE): HandType.FIVE_OF_A_KIND,
    (2, HandType.TWO_PAIR): HandType.FOUR_OF_A_KIND,
    (1, HandType.FOUR_OF_A_KIND): HandType.FIVE_OF_A_KIND,
    (1, HandType.THREE_OF_A_KIND): HandType.FOUR_OF_A_KIND,
    (1, HandType.TWO_PAIR): HandType.FULL_HOUSE,
    (1, HandType.ONE_PAIR): HandType.THREE_OF_A_KIND,
}

JOKER_DEFAULT_UPGRADES = {
    (4): HandType.FIVE_OF_A_KIND,
    (3): HandType.FOUR_OF_A_KIND,
    (2): HandType.THREE_OF_A_KIND,
    (1): HandType.ONE_PAIR,
}

def classify_hand_joker(hand):
    result = group_cards(hand)
    jokers = result.get('J', 0)
    type = group_to_type(result)

    return JOKER_UPGRADES.get((jokers, type), JOKER_DEFAULT_UPGRADES.get(jokers, type))

def classify_hand(hand):
    return group_to_type(group_cards(hand))

def group_to_type(result):
    if len(result) == 1:
        return HandType.FIVE_OF_A_KIND
    elif len(result) == 2:
        if has_group_of_size(result, 4):
            return HandType.FOUR_OF_A_KIND
        else:
            return HandType.FULL_HOUSE
    elif len(result) == 3:
        if has_group_of_size(result, 3):
            return HandType.THREE_OF_A_KIND
        else:
            return HandType.TWO_PAIR
    elif len(result) == 4:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD

def rank_hands(hands, joker=False):
    return sorted(hands, key=lambda hand: (hand.type.value, card_order(hand.cards, joker)))

def card_order(cards, joker=False):
    order = {'T': 10, 'J': 11 if not joker else 0, 'Q': 12, 'K': 13, 'A': 14}
    return tuple(order[c] if c in order else int(c) for c in cards)

def group_cards(s):
    groups = groupby(sorted(s))
    result = {label: sum(1 for _ in group) for label, group in groups}
    return result

def has_jokers(groups):
    return any(label == 'J' for label, _ in groups)

def has_group_of_size(groups, size):
    return any(count == size for count in groups.values())

def total_winnings(hands):
    return sum(hand.bid * (i+1) for i, hand in enumerate(hands))

class TestSolution(unittest.TestCase):
    def test(self):

        # 33332 and 2AAAA: 33332 is stronger
        self.assertEqual(sorted(['33332', '2AAAA'], key=card_order), ['2AAAA', '33332'])
        # 77888 and 77788: 77888 is stronger because its third card is stronger
        self.assertEqual(sorted(['77888', '77788'], key=card_order), ['77788', '77888'])

        self.assertEqual(classify_hand('KTJJT'), HandType.TWO_PAIR)
        self.assertEqual(classify_hand('KK677'), HandType.TWO_PAIR)
        self.assertEqual(classify_hand('QQQJA'), HandType.THREE_OF_A_KIND)
        self.assertEqual(classify_hand('T55J5'), HandType.THREE_OF_A_KIND)

        self.assertEqual(classify_hand_joker('KK677'), HandType.TWO_PAIR)
        self.assertEqual(classify_hand_joker('T55J5'), HandType.FOUR_OF_A_KIND)
        self.assertEqual(classify_hand_joker('KTJJT'), HandType.FOUR_OF_A_KIND)
        self.assertEqual(classify_hand_joker('QQQJA'), HandType.FOUR_OF_A_KIND)

        self.assertEqual(classify_hand_joker('23456'), HandType.HIGH_CARD)
        self.assertEqual(classify_hand_joker('2345J'), HandType.ONE_PAIR)
        self.assertEqual(classify_hand_joker('2344J'), HandType.THREE_OF_A_KIND)
        self.assertEqual(classify_hand_joker('2244J'), HandType.FULL_HOUSE)
        self.assertEqual(classify_hand_joker('2444J'), HandType.FOUR_OF_A_KIND)
        self.assertEqual(classify_hand_joker('4444J'), HandType.FIVE_OF_A_KIND)
        self.assertEqual(classify_hand_joker('234JJ'), HandType.THREE_OF_A_KIND)
        self.assertEqual(classify_hand_joker('244JJ'), HandType.FOUR_OF_A_KIND)
        self.assertEqual(classify_hand_joker('444JJ'), HandType.FIVE_OF_A_KIND)
        self.assertEqual(classify_hand_joker('23JJJ'), HandType.FOUR_OF_A_KIND)
        self.assertEqual(classify_hand_joker('33JJJ'), HandType.FIVE_OF_A_KIND)
        self.assertEqual(classify_hand_joker('3JJJJ'), HandType.FIVE_OF_A_KIND)
        self.assertEqual(classify_hand_joker('JJJJJ'), HandType.FIVE_OF_A_KIND)

        input_data = textwrap.dedent("""
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        ## Part 1
        hands = get_hands(input_data)
        ranked_hands = rank_hands(hands)
        self.assertEqual(ranked_hands[0].cards, '32T3K')
        self.assertEqual(ranked_hands[1].cards, 'KTJJT')
        self.assertEqual(ranked_hands[2].cards, 'KK677')
        self.assertEqual(ranked_hands[3].cards, 'T55J5')
        self.assertEqual(ranked_hands[4].cards, 'QQQJA')
        self.assertEqual(total_winnings(ranked_hands), 6440)

        ## Part 2
        hands = get_hands(input_data, True)
        ranked_hands = rank_hands(hands)
        self.assertEqual(ranked_hands[0].cards, '32T3K')
        self.assertEqual(ranked_hands[1].cards, 'KK677')
        self.assertEqual(ranked_hands[2].cards, 'T55J5')
        self.assertEqual(ranked_hands[3].cards, 'QQQJA')
        self.assertEqual(ranked_hands[4].cards, 'KTJJT')
        self.assertEqual(total_winnings(ranked_hands), 5905)

        input_data = textwrap.dedent("""
        2345A 1
        Q2KJJ 13
        Q2Q2Q 19
        T3T3J 17
        T3Q33 11
        2345J 3
        J345A 2
        32T3K 5
        T55J5 29
        KK677 7
        KTJJT 34
        QQQJA 31
        JJJJJ 37
        JAAAA 43
        AAAAJ 59
        AAAAA 61
        2AAAA 23
        2JJJJ 53
        JJJJ2 41
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        ## Part 1
        hands = get_hands(input_data)
        ranked_hands = rank_hands(hands)
        self.assertEqual(total_winnings(ranked_hands), 6592)

        ## Part 2
        hands = get_hands(input_data, True)
        ranked_hands = rank_hands(hands, True)
        self.assertEqual(total_winnings(ranked_hands), 6839)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()