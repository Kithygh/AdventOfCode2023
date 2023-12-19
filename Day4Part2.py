from pathlib import Path
from dataclasses import dataclass

@dataclass
class Card():
    card_no: int
    winners: int
    copies: int

# input_file = Path("inputs", "day4sample.text")
input_file = Path("inputs", "day4.text")

# take line, extract initial card
def extract_lists(line: str) -> Card:
    winners, _, revealed = line.partition('|')
    card_no, _, winners = winners.partition(':')
    card_no = card_no.split()[-1]
    winners = winners.strip().split()
    revealed = revealed.strip().split()
    winners = len([x for x in winners if x in revealed])
    return Card(card_no, winners, 1)

def get_cards() -> list[Card]:
    cards = []
    with open(input_file) as f:
        for line in f:
            cards.append(extract_lists(line))
    return cards

def process_cards(cards: list[Card]):
    for idx, card in enumerate(cards):
        for x in range(card.winners):
            cards[idx+x+1].copies += card.copies

def calculate_points(cards: list[Card]) -> int:
    points = 0
    for card in cards:
        points += card.copies
    return points

def main():
    cards = get_cards()
    process_cards(cards)
    print(f"Total points: {calculate_points(cards)}")

if __name__ == "__main__":
    main()
