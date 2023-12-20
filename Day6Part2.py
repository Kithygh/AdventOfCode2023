from pathlib import Path
from dataclasses import dataclass


@dataclass
class Race():
    time: int
    distance: int

@dataclass
class Run():
    revtime: int
    distance: int

# input = Path("inputs", "day6sample.text")
input = Path("inputs", "day6.text")

def parse_races() -> Race:
    with input.open() as f:
        lines = f.readlines()
    _, _, times = lines[0].partition(':')
    times = int(times.strip().replace(' ', ''))
    _, _, distances = lines[1].partition(':')
    distances = int(distances.strip().replace(' ', ''))
    return (Race(times, distances))

def find_slowest(race: Race) -> int:
    for x in range(1, race.time):
        distance = (race.time - x) * x
        if distance > race.distance:
            return x

def find_fastest(race: Race) -> int:
    for x in range(race.time-1, 1, -1):
        distance = (race.time - x) * x
        if distance > race.distance:
            return x

def main():
    race = parse_races()
    print(f"{race=}")
    total = 1

    total = find_fastest(race) - find_slowest(race) + 1
    print(f"Race: {race}")
    print(f"Slowest: {find_slowest(race)}")
    print(f"Fastest: {find_fastest(race)}")
    print(f"Total: {total}")

if __name__ == "__main__":
    main()
