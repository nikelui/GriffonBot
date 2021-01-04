import random


class FrenchCard:
    def __init__(self, value, suit):
        """values: 0-13 (1=Ace, 2-10=Numbers, 11=J, 12=Q, 13=K, 0=Joker)
           suits: 0=Hearts, 1=Diamonds, 2=Clover, 3=Spades
           Joker: 0=red, 1=black
        """
        self.value = value
        self.suit = suit


class FrenchDeck:
    def __init__(self, joker=True):
        self.cards = []
        if joker:
            cards.append(FrenchCard(0, 0))
            cards.append(FrenchCard(0, 1))
        for i in range(1,14):
            for j in range(4):
                self.cards.append(FrenchCard(i, j))

    def shuffle(self):
        random.shuffle(self.cards)
    
    def deal(self, n=1):
        to_deal = []
        for i in range(n):
            to_deal.append(self.cards.pop())
        return to_deal
