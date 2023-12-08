from pathlib import Path

input_file = Path("inputs", "d1p1.text")
written_numbers = ["one","two","three","four","five","six","seven","eight","nine"]

def find_first_digit(line: str) -> tuple[int,int]:
    for idx, char in enumerate(line):
        if char.isnumeric():
            return (int(char))
        for num in written_numbers:
            if line.startswith(num, idx):
                return written_numbers.index(num)+1

def find_second_digit(line: str) -> tuple[int,int]:
    for idx, char in enumerate(line[::-1]):
        if char.isnumeric():
            return int(char)
        for num in written_numbers:
            if line.startswith(num, len(line)-idx-1):
                return written_numbers.index(num)+1

total = 0
with open(input_file) as f:
    for line in f:
        digit1 = find_first_digit(line)
        digit2 = find_second_digit(line)
        total += int(f"{digit1}{digit2}")
    print(total)
