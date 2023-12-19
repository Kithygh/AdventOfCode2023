from pathlib import Path

input_file = Path("inputs", "d1p1.text")

total = 0
with open(input_file) as f:
    for line in f:
        for char in line:
            if char.isnumeric():
                first_num = char
                break
        for char in line[::-1]:
            if char.isnumeric():
                second_num = char
                break
        print(f"{first_num}{second_num}")
        total += int(f"{first_num}{second_num}")
        print(total)
