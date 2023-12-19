from pathlib import Path
from collections import namedtuple

# input_file = Path("inputs", "day2sample.text")
input_file = Path("inputs", "day2.text")

RGB = namedtuple('RGB', ['red', 'green', 'blue'])

# given game, find each round
def find_rounds(line: str) -> list[str]:
    line = line.rstrip()
    _, _, rounds = line.partition(': ')
    return rounds.split('; ')

# given rounds, find tuple of cubes
def parse_round(round: str) -> RGB:
    cubes = round.split(', ')
    # print(cubes)
    red = 0
    blue = 0
    green = 0
    for cube in cubes:
        num, _, color = cube.partition(' ')
        # print(f"|{color}|")
        match color:
            case "red":
                red = int(num)
            case "green":
                green = int(num)
            case "blue":
                blue = int(num)
    return RGB(red,green,blue)

# given list of RGB, find max of r and g and b
def max_rgb(rgbs: list[RGB]) -> RGB:
    def max_color(rgbs: list[RGB], color: str) -> RGB:
        count = 0
        for rgb in rgbs:
            # count = max([rgb[color], count])
            if color == "red":
                if rgb.red > count:
                    count = rgb.red
            if color == "green":
                if rgb.green > count:
                    count = rgb.green
            if color == "blue":
                if rgb.blue > count:
                    count = rgb.blue
        return count
    red = max_color(rgbs, "red")
    green = max_color(rgbs, "green")
    blue = max_color(rgbs, "blue")
    return RGB(red, green, blue)

# given max rgb, find if game is possible
def is_possible(input: RGB, max: RGB) -> bool:
    if input.red > max.red:
        return False
    if input.green > max.green:
        return False
    if input.blue > max.blue:
        return False
    return True


with open(input_file) as f:
    game_count = 0
    result = 0
    max_cubes = RGB(12, 13, 14)

    for game in f:
        game_count += 1
        rounds = find_rounds(game)
        # print(rounds)
        parsed_rounds = []
        for round in rounds:
            parsed_rounds.append(parse_round(round))

        largest = max_rgb(parsed_rounds)
        if is_possible(largest, max_cubes):
            result += game_count
        # print(f"{parsed_round=}")
    print(result)
