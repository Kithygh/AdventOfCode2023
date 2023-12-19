from dataclasses import dataclass
from itertools import islice
from pathlib import Path
import collections

# input_file = Path("inputs", "day3sample.text")
input_file = Path("inputs", "day3.text")

@dataclass
class part_number():
    value: int
    length: int
    start_idx: int


def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(islice(it, n-1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)

def find_numbers(line: str) -> list[part_number]:
    state = "run"
    current_number = ""
    part_numbers = []
    start_idx = 0
    for idx, char in enumerate(line):
        match state:
            case "run":
                if char.isnumeric():
                    state = "add"
                    current_number += char
                    start_idx = idx
                else:
                    pass
            case "add":
                if char.isnumeric():
                    current_number += char
                else:
                    state = "run"
                    part_numbers.append(part_number(value=int(current_number), length=len(current_number), start_idx=start_idx))
                    current_number = ""
    return part_numbers

def verify_part_number(triple: tuple, part: part_number) -> bool:
    safe = ['0','1','2','3','4','5','6','7','8','9','.']
    start = max([part.start_idx-1, 0])
    end = min([part.start_idx+part.length+1, len(triple[1])-1])
    for line in triple:
        line = line.rstrip()
        for x in range(start, end):
            if line[x] not in safe:
                return True
    return False

def main():
    total = 0
    with open(input_file) as f:
        lines = []
        lines.append('.'*140 + '\n')
        lines += f.readlines()
        lines.append('.'*140 + '\n')
        for triple in sliding_window(lines, 3):
            numbers_on_line = find_numbers(triple[1])
            for number in numbers_on_line:
                if verify_part_number(triple, number):
                    total += number.value
    print(f"{total=}")

if __name__ == "__main__":
    main()
