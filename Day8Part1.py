from pathlib import Path
from itertools import cycle

# input = Path("inputs", "day8sample.text")
input = Path("inputs", "day8.text")

def get_directions_nodes():
    with input.open() as f:
        lines = f.readlines()

    directions = []
    for char in lines[0]:
        if char == 'L':
            directions.append(0)
        if char == 'R':
            directions.append(1)

    lines = lines[2:]
    nodes = {}
    for line in lines:
        label, _, dests = line.partition(' = (')
        dests = dests.strip()[0:-1]
        left, _, right = dests.partition(', ')
        dirs = []
        dirs.append(left)
        dirs.append(right)
        nodes[label] = dirs

    return directions, nodes

def main():
    directions, nodes = get_directions_nodes()

    count = 0
    label = 'AAA'
    dir_sequence = cycle(directions)
    for dir in dir_sequence:
        label = nodes[label][dir]
        count += 1
        if label == 'ZZZ':
            print(f"{count=}")
            break

if __name__ == "__main__":
    main()
