from pathlib import Path
from itertools import cycle
from math import lcm

# input = Path("inputs", "day8sample2.text")
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

def find_starting_nodes(nodes: dict[str, list]) -> list[str]:
    starters = []
    for label in nodes.keys():
        if label.endswith('A'):
            starters.append(label)
    return starters

def main():
    directions, nodes = get_directions_nodes()

    current_nodes = find_starting_nodes(nodes)
    count = 0
    dir_sequence = cycle(directions)
    node_cycles = []
    for label in current_nodes:
        count = 0
        dir_sequence = cycle(directions)
        for dir in dir_sequence:
            label = nodes[label][dir]
            count += 1
            if label.endswith('Z'):
                node_cycles.append(count)
                break

    result = lcm(*node_cycles)
    print(F"{result=}")

if __name__ == "__main__":
    main()
