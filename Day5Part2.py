from pathlib import Path
from dataclasses import dataclass

# input_file = Path("inputs", "day5sample.text")
input_file = Path("inputs", "day5.text")

@dataclass
class Bounds():
    start: int
    end: int

    def __lt__(self, other):
        return self.start < other.start

class Mapping():
    # source: Bounds
    # dest: Bounds

    def __init__(self, source:Bounds, dest:Bounds):
        assert source.end - source.start == dest.end - dest.start
        self.source = source
        self.dest = dest


seeds: list[Bounds] = []
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
    seeds = extract_seed_ranges(lines.pop(0))

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
                if j.source.start < i.source.start:
                    assert j.source.end < i.source.start
                if j.source.start > i.source.start:
                    assert j.source.start > i.source.end

def extract_seed_ranges(line: str) -> list[Bounds]:
    _, _, line = line.partition(':')
    seeds = line.strip().split()
    nums = [int(x) for x in seeds]
    seeds: list[Bounds] = []
    for x in range(0, len(nums), 2):
        seeds.append(Bounds(nums[x], nums[x]+nums[x+1]))
    return seeds

def extract_mapping(line: str) -> Mapping:
    nums = line.strip().split()
    range = int(nums[2])
    source_start = int(nums[1])
    source_end = source_start + range -1
    dest_start = int(nums[0])
    dest_end = dest_start + range -1
    return Mapping(Bounds(source_start, source_end), Bounds(dest_start, dest_end))

def print_almanac():
    print(f"{seeds=}")
    for page, mapping in zip(names, mappings):
        print(f"{page}")
        for m in mapping:
            print(m)

def convert(chunks: list[Bounds], curr_map: list[Mapping]) -> list[Bounds]:
    # print(f"{chunks=}")
    unconverted = chunks
    converted = []
    for m in curr_map:
        temp_unconverted = []
        if unconverted: # we may have converted all chunks
            for current_chunk in unconverted:
                c, unc = compare_ranges(current_chunk, m)
                converted.append(c)
                temp_unconverted.extend(unc)
        unconverted = temp_unconverted
    converted.extend(unconverted)
    a = [x for x in converted if x != None]
    return a

def test_compare_ranges():
    sm_left = Bounds(1,2)
    sm_right = Bounds(3,4)
    sm_center = Bounds(2,3)
    med_left = Bounds(1,3)
    med_right = Bounds(2,4)
    large = Bounds(1,4)
    sm_dest = Bounds(1000, 1001)
    med_dest = Bounds(1000, 1002)
    large_dest = Bounds(1000, 1003)
    # combos = list(itertools.permutations(["sm_left", "sm_right", "sm_center", "med_left", "med_right", "large"], 2))
    # print(combos)
    # exit()

    c, unc = compare_ranges(sm_left, Mapping(sm_right, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0] == sm_left
        assert c == None
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_left, Mapping(sm_center, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 1
        assert unc[0].end == 1
        assert c.start == 1000
        assert c.end == 1000
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_left, Mapping(med_left, med_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_left, Mapping(med_right, med_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 1
        assert unc[0].end == 1
        assert c.start == 1000
        assert c.end == 1000
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_left, Mapping(large, large_dest))
    try:
        assert len(unc) == 0
        # assert unc[0].start == 1
        # assert unc[0].end == 1
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_right, Mapping(sm_left, sm_dest))
    try:
        assert len(unc) == 1
        assert c == None
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_right, Mapping(sm_center, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 4
        assert unc[0].end == 4
        assert c.start == 1001
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_right, Mapping(med_left, med_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 4
        assert unc[0].end == 4
        assert c.start == 1002
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_right, Mapping(med_right, med_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1001
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_right, Mapping(large, large_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1002
        assert c.end == 1003
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_center, Mapping(sm_left, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 3
        assert unc[0].end == 3
        assert c.start == 1001
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_center, Mapping(sm_right, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 2
        assert unc[0].end == 2
        assert c.start == 1000
        assert c.end == 1000
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_center, Mapping(med_left, med_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1001
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_center, Mapping(med_right, med_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(sm_center, Mapping(large, large_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1001
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_left, Mapping(sm_left, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 3
        assert unc[0].end == 3
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_left, Mapping(sm_right, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 1
        assert unc[0].end == 2
        assert c.start == 1000
        assert c.end == 1000
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_left, Mapping(sm_center, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 1
        assert unc[0].end == 1
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_left, Mapping(med_right, med_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 1
        assert unc[0].end == 1
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_left, Mapping(large, large_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1000
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_right, Mapping(sm_left, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 3
        assert unc[0].end == 4
        assert c.start == 1001
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_right, Mapping(sm_right, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 2
        assert unc[0].end == 2
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_right, Mapping(sm_center, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 4
        assert unc[0].end == 4
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_right, Mapping(med_left, med_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 4
        assert unc[0].end == 4
        assert c.start == 1001
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(med_right, Mapping(large, large_dest))
    try:
        assert len(unc) == 0
        assert c.start == 1001
        assert c.end == 1003
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(large, Mapping(sm_left, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 3
        assert unc[0].end == 4
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(large, Mapping(sm_right, sm_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 1
        assert unc[0].end == 2
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(large, Mapping(sm_center, sm_dest))
    try:
        assert len(unc) == 2
        assert unc[0].start == 1
        assert unc[0].end == 1
        assert unc[1].start == 4
        assert unc[1].end == 4
        assert c.start == 1000
        assert c.end == 1001
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(large, Mapping(med_left, med_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 4
        assert unc[0].end == 4
        assert c.start == 1000
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise

    c, unc = compare_ranges(large, Mapping(med_right, med_dest))
    try:
        assert len(unc) == 1
        assert unc[0].start == 1
        assert unc[0].end == 1
        assert c.start == 1000
        assert c.end == 1002
    except AssertionError:
        print(f"{c=}, {unc=}"); raise


def compare_ranges(bound_in: Bounds, other: Mapping) -> tuple[Bounds, list[Bounds]]:
    # takes two ranges. Return a tuple where the first item is a converted range from the overlap, and second is any unconverted portion(s)
    # tuple(converted, [unconverted1, unconverted2, ...])
    try:
        # if they don't overlap at all, return the unconverted whole
        if bound_in.start > other.source.end or bound_in.end < other.source.start:
            # c, unc = compare_ranges(sm_right, Mapping(sm_center, sm_dest))
            # print("nooverlap")
            return (None, [bound_in,])

        # if the bound is completely in other, return the converted only
        if bound_in.start >= other.source.start and bound_in.end <= other.source.end:
            # print("bound completely in other")
            converted_start = other.dest.start + bound_in.start - other.source.start
            converted_end =   other.dest.start + bound_in.end - other.source.start
            converted = Bounds(converted_start, converted_end)
            return (converted, [])

        # if bound encompasses other without edges lining up
        if bound_in.start < other.source.start and bound_in.end > other.source.end:
            # print("bound encompasses other")
            part1 = Bounds(bound_in.start, other.source.start-1)
            part3 = Bounds(other.source.end+1, bound_in.end)
            converted_start = other.dest.start
            converted_end   = other.dest.end
            converted = Bounds(converted_start, converted_end)
            return (converted, [part1, part3])

        # if both edges line up, just return the dest
        if bound_in.start == other.source.start and bound_in.end == other.source.end:
            return (other.dest, [])

        # if bound overlaps end of other
        if other.source.start <= bound_in.start <= other.source.end:
            assert bound_in.end > other.source.end # if false, this case should be grabbed by the 'other encompasses bound'
            # print("overlaps end")
            unconverted = Bounds(other.source.end+1, bound_in.end)
            converted_start = other.dest.start + bound_in.start - other.source.start
            converted_end = other.dest.end
            converted = Bounds(converted_start, converted_end)
            return (converted, [unconverted,])

        # if bound overlaps beginning of other
        if bound_in.start <= other.source.start <= bound_in.end:
            assert bound_in.end <= other.source.end
            # print("overlaps beginning")
            unconverted = Bounds(bound_in.start, other.source.start - 1)
            converted_start = other.dest.start
            converted_end = other.dest.start + bound_in.end - other.source.start
            converted = Bounds(converted_start, converted_end)
            return (converted, [unconverted,])
        raise NotImplementedError # shouldn't get here!
    except AssertionError as e:
        print(F"{bound_in=}")
        print(F"{other.source=}")
        print(F"{other.dest=}")
        raise



def seed_to_location(seed: Bounds) -> Bounds:
    seeds = [seed, ]
    for m in mappings:
        seeds = convert(seeds, m)
    return seeds

def find_location_ranges() -> list[Bounds]:
    locations = []
    for seed in seeds:
        locations.extend(seed_to_location(seed))
    return locations

def main():
    populate_mappings()
    verify_ranges()
    # print_almanac()
    test_compare_ranges()
    # print(seeds)


    locations = find_location_ranges()
    final = locations[0].start
    for loc in locations:
        if loc.start < final:
            final = loc.start
    print(f"{final=}")


if __name__ == "__main__":
    main()
