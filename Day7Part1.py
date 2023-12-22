from pathlib import Path

# input = Path("inputs", "day7sample.text")
input = Path("inputs", "day7.text")

CARDS = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']

class Hand():
    cards: str
    card_values: list[int]
    counts: list[int]
    bid: int
    score: int
    power: int

    def __init__(self, cards:str, bid:int):
        self.cards = cards
        self.bid = bid
        self.calc_values()
        self.calc_counts()
        self.calc_score()
        self.calc_power()

    def __str__(self):
        return f"cards={self.cards}, power={self.power}, card_values={self.card_values}, counts={self.counts}, bid={self.bid}, score={self.score}, rank={self.power}"

    def __lt__(self, other):
        assert isinstance(other, Hand)
        # print(type(other))
        if self.power != other.power:
            return self.power < other.power
        return self.score < other.score


    def calc_values(self):
        self.card_values = []
        for card in self.cards:
            self.card_values.append(CARDS.index(card))

    def calc_counts(self):
        temp_dict = {}
        for card in self.cards:
            if card in temp_dict:
                temp_dict[card] += 1
            else:
                temp_dict[card] = 1
        temp_list = list(temp_dict.values())
        temp_list.sort(reverse=True)
        self.counts = temp_list
        assert len(self.counts) > 0
        assert len(self.counts) < 6

    def calc_score(self) -> int:
        self.score = 0
        for idx, card in enumerate(reversed(self.card_values)):
            self.score += card * (13 ** idx)

    def calc_power(self):
        # 5, 4, fh, 3, 2p, 1p, high
        self.power = 'blank'
        match self.counts[0]:
            case 5:
                self.power = 7
            case 4:
                self.power = 6
            case 3:
                if self.counts[1] == 2:
                    self.power = 5
                else:
                    self.power = 4
            case 2:
                if self.counts[1] == 2:
                    self.power = 3
                else:
                    self.power = 2
            case 1:
                self.power = 1
            case _:
                raise ValueError
        assert self.power in [1,2,3,4,5,6,7]

def get_hands() -> list[Hand]:
    hands = []
    with input.open() as f:
        lines = f.readlines()
    for line in lines:
        text = line.split()
        hands.append(Hand(text[0], int(text[1])))
    return hands

def main():
    hands = get_hands()
    hands.sort()
    total = 0
    for idx, hand in enumerate(hands, start=1):
        total += hand.bid * idx
    print(total)


if __name__ == "__main__":
    main()
