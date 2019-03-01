from enum import Enum
from functools import reduce
from operator import mul


class Color(Enum):
    RED = 1,
    GREEN = 2,
    BLUE = 3,
    YELLOW = 4


class Attribute(Enum):
    HP = 1,
    ATK = 2,
    DF = 3,
    SPEED = 4


class Rule(Enum):
    ADD = 1,
    MULTIPLY = 2,
    SUBTRACT = 3


class Card:
    def __init__(self, color, value):
        self.color = color
        self.value = value


class Move:
    def __init__(self, color_one, color_two, rule):
        self.color_one = color_one
        self.color_two = color_two
        self.rule = rule

    def execute(self, cards):
        value_one = reduce(mul, [i.value for i in cards if i.color is self.color_one])
        value_two = reduce(mul, [i.value for i in cards if i.color is self.color_two])

        if self.rule is Rule.ADD:
            return value_one + value_two
        elif self.rule is Rule.MULTIPLY:
            return value_one * value_two
        elif self.rule is Rule.SUBTRACT:
            return value_one - value_two
        else:
            return 0


class Minion:
    def __init__(self, hp_color, atk_color, df_color, speed_color):
        self.stats = {Attribute.HP :   hp_color,
                      Attribute.ATK:   atk_color,
                      Attribute.DF:    df_color,
                      Attribute.SPEED: speed_color}
        self.cards = []
        self.moves = {"supa kicka": Move(Color.RED, Color.RED, Rule.ADD)}

    def get_stat(self, stat):
        stat_color = self.stats[stat]
        stat_value = reduce(mul, [i.value for i in self.cards if i.color is stat_color])

        return stat_value

    def execute_move(self, move_name):
        return self.moves[move_name].execute(self.cards)


my_minion = Minion(Color.RED, Color.RED, Color.GREEN, Color.GREEN)
my_minion.cards.append(Card(Color.RED, 5))
print(my_minion.get_stat(Attribute.ATK))
print(my_minion.execute_move("supa kicka"))
