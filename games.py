# Script containing game logics

import random
import d20


class diceIterClass:
    """Class to iterate through the dice expressions"""
    def __init__(self, obj):
        self.children = []
        self.initial_rolls = {}
        self.crossdoom_rolls = {}
        self.obj = obj
        self.traverse_expression(self.obj)
        self.fill_dict()
  
    def traverse_expression(self, obj):
        if isinstance(obj, d20.expression.BinOp):
             self.children.insert(0, obj.right)
             self.traverse_expression(obj.left)
        elif isinstance(obj, d20.expression.Dice):
             self.children.insert(0, obj)
    
    def fill_dict(self):
        self.initial_rolls['int'] = []
        self.crossdoom_rolls['int'] = []
        # start by filling the initial_rolls dict
        for dice in self.children:
            # if the current roll is a Dice
            if isinstance(dice, d20.expression.Dice):
                self.initial_rolls[dice.size] = []
                self.crossdoom_rolls[dice.size] = []
                for die in dice.values:  # loop through single dies    
                    self.initial_rolls[dice.size].append(die.values[0].values[0])
                    self.crossdoom_rolls[dice.size].append(die.values[0].values[0])
                self.initial_rolls[dice.size].sort()
                self.crossdoom_rolls[dice.size].sort()
            elif isinstance(dice, d20.expression.Literal):
                self.initial_rolls['int'].append(dice.values[0])
                self.crossdoom_rolls['int'].append(dice.values[0])
        # now loop through the rolls and apply Crossdoom rules
        for key in self.crossdoom_rolls.keys():
            if isinstance(key, int):  # process only dices
                # First, remove one good result for each '1'
                if len(self.crossdoom_rolls[key]) > 0:
                    while (self.crossdoom_rolls[key][0] == 1 and 
                           len(self.crossdoom_rolls[key]) >= 1):
                        if len(self.crossdoom_rolls[key]) >= 2:
                            _ = self.crossdoom_rolls[key].pop(-1)
                        _ = self.crossdoom_rolls[key].pop(0)
                # Now, explode results once
                to_explode = sum([x == key for x in self.crossdoom_rolls[key]])
                for _i in range(to_explode):
                    self.crossdoom_rolls[key].append(random.randint(1,key))


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
