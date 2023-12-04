import sys
import textwrap
import unittest

def run():
    with open("./input/2023-d03-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    schematic = read_schematic(input_data)
    [part_numbers, gears] = read_part_numbers(schematic)
    print(part_numbers)

    print("** Part 1 Final: ", sum(part_numbers))
    print("** Part 2 Final: ", gear_ratios(gears))

# add up all the part numbers
# any number adjacent to a symbol, even diagonally, is a "part number" 
# and should be included in your sum
# Periods (.) do not count as a symbol

def read_part_numbers(schematic):
    part_numbers = []
    gears = {}
    n_begin = -1
    n_end = -1
    for r, value in enumerate(schematic): # row
        for c, value in enumerate(schematic[r]): # column   
            if value.isnumeric():
                if n_begin == -1:
                    n_begin = c
                n_end = c
            else:
                if n_begin != -1:
                    part_number = is_a_part_number(schematic, r, n_begin, n_end, gears)
                    if part_number != None:
                        part_numbers.append(part_number)
                    n_begin = -1
                    n_end = -1

        # Are we in the middle of a number at the end of the row?
        if n_begin != -1:
            part_number = is_a_part_number(schematic, r, n_begin, n_end, gears)
            if part_number != None:
                part_numbers.append(part_number)
            n_begin = -1
            n_end = -1

    gears = dict(filter(lambda item: len(item[1]) == 2, gears.items()))
    return [part_numbers, gears]

def is_a_part_number(schematic, row, n_begin, n_end, gears):
    min_y = row if row == 0 else row - 1
    max_y = row if row == len(schematic) - 1 else row + 2
    min_x = n_begin if n_begin == 0 else n_begin - 1
    max_x = n_end if n_end == len(schematic[0]) - 1 else n_end + 2

    for r in range(min_y, max_y):
        for c in range(min_x, max_x):
            if schematic[r][c] == '.' or schematic[r][c].isnumeric():
                continue
            else:
                num = int(''.join(schematic[row][n_begin:n_end+1]))
                if schematic[r][c] == '*':
                    gears[(r,c)] = gears.get((r, c), [])
                    gears[(r, c)].append(num)
                return num
    return None

def gear_ratios(gears):
    result = 0
    for value in gears.values():
        result += value[0]*value[1]
    return result
    

# Make a list of lists of characters
def read_schematic(input_data):
    schematic = [list(line) for line in input_data]
    return schematic

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
        467..114..
        ...*......
        ..35..633.
        ......#...
        617*......
        .....+.58.
        ..592.....
        ......755.
        ...$.*....
        .664.598..
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        schematic = read_schematic(input_data)
        [part_numbers, gears] = read_part_numbers(schematic)
        self.assertEqual(part_numbers, [467, 35, 633, 617, 592, 755, 664, 598])
        self.assertEqual(sum(part_numbers), 4361)
        
        result = gear_ratios(gears)
        self.assertEqual(result, 467835)


if __name__ == "__main__":
    # Run unit tests if the script was run with the --test argument
    if '--test' in sys.argv:
        unittest.main(argv=['first-arg-is-ignored'], exit=False)
    else:
        run()