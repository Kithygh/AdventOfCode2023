from pathlib import Path

# input_file = Path("inputs", "day4sample.text")
input_file = Path("inputs", "day4.text")

# take line, extract list of winners and list of revealed
def extract_lists(line: str) -> tuple[list[int], list[int]]:
    winners, _, revealed = line.partition('|')
    _, _, winners = winners.partition(':')
    winners = winners.strip().split()
    revealed = revealed.strip().split()
    return winners, revealed


# take list of winners and revealed, return number of matches
def count_matches(winners: list[int], revealed: list[int]):
    thing = [x for x in winners if x in revealed]
    return len(thing)

def main():
    points = 0
    with open(input_file) as f:
        for line in f:
            if (winner_count := count_matches(*extract_lists(line))):
                points += 2 ** (winner_count-1)
    print(f"Total points: {points}")

if __name__ == "__main__":
    main()
