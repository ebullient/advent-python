import unittest
import textwrap

def run():
    with open("./input/2023-d01-input.txt", 'r') as file:
        input_data = [line.strip() for line in file.readlines()]

    print("** Part 1 Final: ", calibrate(input_data))
    print("** Part 2 Final: ", calibrate_2(input_data))
    
def prep_value(input_string):
    replacements = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    i = 0
    result = ''
    while i < len(input_string):
        if input_string[i].isdigit():
            result += input_string[i]
            i += 1
            continue
        found = False
        for( key, value ) in replacements.items():
            if input_string[i:i+len(key)] == key:
                found = True
                result += value
                i += len(key) - 1
                break
        if not found:
            i += 1
    return result

def find_value(input_string):
    result = ''
    # Your code goes here
    for char in input_string:
        if char.isdigit():
            result += char
            break;
    for char in reversed(input_string):
        if char.isdigit():
            result += char
            break;
    return int(result)

def calibrate(input_data):
    result = 0
    for input_string in input_data:
        result += find_value(input_string)
    return result

def calibrate_2(input_data):
    result = 0
    for input_string in input_data:
        result += find_value(prep_value(input_string))
    return result

class TestSolution(unittest.TestCase):
    def test(self):
        input_data = textwrap.dedent("""
            1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines
        
        # Part 1: first digit and the last digit (in that order, of each line) to form a single two-digit number.
        # For these four lines: 12, 38, 15, and 77. 
        # Adding these together produces 142.
        self.assertEqual(find_value(input_data[0]), 12)
        self.assertEqual(find_value(input_data[1]), 38)
        self.assertEqual(find_value(input_data[2]), 15)
        self.assertEqual(find_value(input_data[3]), 77)
        self.assertEqual(calibrate(input_data), 142)
    
    def test_2(self):
        # Part 2: uh.. nope! Some numbers are spelled out.
        input_data = textwrap.dedent("""
            two1nine
            eightwothree
            abcone2threexyz
            xtwone3four
            4nineeightseven2
            zoneight234
            7pqrstsixteen
        """).split('\n')[1:-1]  # split by newline and remove the first and last empty lines

        self.assertEqual(prep_value(input_data[0]), "219")
        self.assertEqual(prep_value(input_data[1]), "823")
        self.assertEqual(prep_value(input_data[2]), "123")
        self.assertEqual(prep_value(input_data[3]), "2134")
        self.assertEqual(prep_value(input_data[4]), "49872")
        self.assertEqual(prep_value(input_data[5]), "18234")
        self.assertEqual(prep_value(input_data[6]), "76")
        
        self.assertEqual(find_value(prep_value(input_data[0])), 29)
        self.assertEqual(find_value(prep_value(input_data[1])), 83)
        self.assertEqual(find_value(prep_value(input_data[2])), 13)
        self.assertEqual(find_value(prep_value(input_data[3])), 24)
        self.assertEqual(find_value(prep_value(input_data[4])), 42)
        self.assertEqual(find_value(prep_value(input_data[5])), 14)
        self.assertEqual(find_value(prep_value(input_data[6])), 76)
        
        self.assertEqual(calibrate_2(input_data), 281)
        

if __name__ == "__main__":
    # Run the main function
    run()
    # Run unit tests
    unittest.main()