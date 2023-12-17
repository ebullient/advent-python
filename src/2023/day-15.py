from collections import deque, namedtuple
from functools import cache
import sys
import textwrap
import unittest

def run():
    with open("./input/2023-d15-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    inputs = input_data[0].split(',')
    array = MirrorArray()
    array.arrange_mirrors(inputs)
    _, power = array.focus_power()

    print("** Part 1 Final: ", hashAll(inputs))
    print("** Part 2 Final: ", power)

Mirror = namedtuple('Mirror', ['label', 'focal'])

class MirrorArray:
    def __init__(self):
        self.array = [deque() for _ in range(256)]

    def arrange_mirrors(self, inputs):
        for input in inputs:
            self.mirror_step(input)

    def mirror_step(self, input):
        if input.endswith('-'):
            label = input[:-1]
            i = hashString(label)
            box = self.array[i]
            for m in list(box):
                if m.label == label:
                    box.remove(m)
                    break
        else:
            label, focal = input.split('=')
            mirror = Mirror(label, int(focal))
            i = hashString(label)
            box = self.array[i]
            for j, m in enumerate(box):
                if m.label == label:
                    box[j] = mirror
                    break
            else:
                box.append(mirror)

    def focus_power(self):
        lenses = dict()
        total = 0
        for i in range(256):
            box = self.array[i]
            for j, m in enumerate(box):
                power = (1+i) * (j+1) * m.focal
                lenses[m.label] = power
                total += power
        return lenses, total

    def test_box(self, i):
        return self.array[i]

def hashAll(input):
    return sum([hashString(x) for x in input])

@cache
def hashString(str):
    current = 0
    for char in list(str):
        current = hashStep(current, char)
    return current

def hashStep(current, char):
    current += ord(char)
    current *= 17
    current %= 256
    return current

class TestSolution(unittest.TestCase):
    def test(self):
        self.assertEqual(hashString('HASH'), 52)

        input_data = textwrap.dedent("""
        rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        input = input_data[0].split(',')

        self.assertEqual(hashString(input[0]), 30)
        self.assertEqual(hashString(input[1]), 253)
        self.assertEqual(hashString(input[2]), 97)
        self.assertEqual(hashString(input[3]), 47)
        self.assertEqual(hashString(input[4]), 14)
        self.assertEqual(hashString(input[5]), 180)
        self.assertEqual(hashString(input[6]), 9)
        self.assertEqual(hashString(input[7]), 197)
        self.assertEqual(hashString(input[8]), 48)
        self.assertEqual(hashString(input[9]), 214)
        self.assertEqual(hashString(input[10]), 231)

        self.assertEqual(hashAll(input), 1320)

        mirrors = MirrorArray()

        mirrors.mirror_step(input[0])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1)])
        mirrors.mirror_step(input[1])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1)])
        mirrors.mirror_step(input[2])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1)])
        self.assertEqual(mirrors.test_box(1), [Mirror('qp', 3)])
        mirrors.mirror_step(input[3])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(1), [Mirror('qp', 3)])
        mirrors.mirror_step(input[4])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(1), [])
        mirrors.mirror_step(input[5])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(3), [Mirror('pc', 4)])
        mirrors.mirror_step(input[6])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(3), [Mirror('pc', 4), Mirror('ot', 9)])
        mirrors.mirror_step(input[7])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(3), [Mirror('pc', 4), Mirror('ot', 9), Mirror('ab', 5)])
        mirrors.mirror_step(input[8])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(3), [Mirror('ot', 9), Mirror('ab', 5)])
        mirrors.mirror_step(input[9])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(3), [Mirror('ot', 9), Mirror('ab', 5), Mirror('pc', 6)])
        mirrors.mirror_step(input[10])
        self.assertEqual(mirrors.test_box(0), [Mirror('rn', 1), Mirror('cm', 2)])
        self.assertEqual(mirrors.test_box(3), [Mirror('ot', 7), Mirror('ab', 5), Mirror('pc', 6)])

        lenses, total = mirrors.focus_power()
        self.assertEqual(lenses['rn'], 1)
        self.assertEqual(lenses['cm'], 4)
        self.assertEqual(lenses['ot'], 28)
        self.assertEqual(lenses['ab'], 40)
        self.assertEqual(lenses['pc'], 72)
        self.assertEqual(total, 145)

if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()
