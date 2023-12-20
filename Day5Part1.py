from pathlib import Path
from dataclasses import dataclass

# input_file = Path("inputs", "day5sample.text")
input_file = Path("inputs", "day5.text")

@dataclass
class Mapping():
    source_start: int
    dest_start: int
    range: int

seeds = []
seed_to_soil: list[Mapping] = []
soil_to_fertilizer: list[Mapping] = []
fertilizer_to_water: list[Mapping] = []
water_to_light: list[Mapping] = []
light_to_temperature: list[Mapping] = []
temperature_to_humidity: list[Mapping] = []
humidity_to_location: list[Mapping] = []

names = ("seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location")
mappings = [seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location]

def populate_mappings():
    with open(input_file) as f:
        lines = f.readlines()
    global seeds
    seeds = extract_seeds(lines.pop(0))

    global mappings
    current_mapping = -1
    for line in lines:
        if line == '\n':
            continue
        if line.startswith(names):
            current_mapping += 1
            continue
        new_mapping = extract_mapping(line)
        mappings[current_mapping].append(new_mapping)

def verify_ranges():
    for m in mappings:
        for i in m:
            for j in m:
                if j.source_start < i.source_start:
                    assert (j.source_start + j.range - 1) < i.source_start
                if j.source_start > i.source_start:
                    assert j.source_start > (i.source_start + i.range - 1)

def extract_seeds(line: str) -> list[int]:
    _, _, line = line.partition(':')
    seeds = line.strip().split()
    return [int(x) for x in seeds]

def extract_mapping(line: str) -> Mapping:
    nums = line.strip().split()
    range = int(nums[2])
    source_start = int(nums[1])
    dest_start = int(nums[0])
    return Mapping(source_start, dest_start, range)

def print_almanac():
    print(f"{seeds=}")
    for page, mapping in zip(names, mappings):
        print(f"{page}")
        for m in mapping:
            print(m)


def convert(source: int, curr_map: list[Mapping]) -> int:
    for m in curr_map:
        if source in range(m.source_start, m.source_start + m.range):
            return (source - m.source_start + m.dest_start)
    return source

def seed_to_location(seed: int) -> int:
    for m in mappings:
        seed = convert(seed, m)
    return seed

def find_locations() -> list[int]:
    locations = []
    for seed in seeds:
        locations.append(seed_to_location(seed))
    return locations

def main():
    populate_mappings()
    verify_ranges()
    # print_almanac()
    locations = find_locations()
    print(f"Lowest location number: {min(locations)}")

if __name__ == "__main__":
    main()
