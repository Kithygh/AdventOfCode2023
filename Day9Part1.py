from pathlib import Path
from functools import cache
from itertools import pairwise
from dataclasses import dataclass

# input = Path("inputs", "day9sample.text")
input = Path("inputs", "day9.text")

@dataclass
class DataLine():
    ends: int
    current_layer: list[int]



def get_starting_data() -> list[DataLine]:
    inputs = []
    with input.open() as f:
        lines = f.readlines()

    for line in lines:
        nums = [int(x) for x in line.strip().split()]
        inputs.append(DataLine(nums[-1], nums ))
    return inputs


# @cache
def get_next_layer_down(*args):
    layer = []
    for a, b in pairwise(args):
        layer.append(b-a)
    if not any(layer):
        return 0
    # print(f"intermediate layer: {layer}")
    return layer



def main():
    datas = get_starting_data()
    for data in datas:
        layer = data.current_layer
        while layer:
            if (layer := get_next_layer_down(*layer)):
                data.current_layer = layer
                data.ends += layer[-1]
    total = 0
    for data in datas:
        total += data.ends
    print(f"{total=}")
if __name__ == "__main__":
    main()
