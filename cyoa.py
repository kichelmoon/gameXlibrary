from typing import List, Any

CHOICE_TYPE_ONCE = 1
CHOICE_TYPE_IF = 2
CHOICE_TYPE_PERMANENT = 3


class Effect:
    def __init__(self, text, state_change, next_node):
        """
        :type text: str
        :type state_change: dict
        :type next_node: str
        """
        self.text = text
        self.state_change = state_change
        self.next_node = next_node


class Choice:
    """
    :type choice_type: int
    :type description: str
    :type effect: Effect
    :type condition: dict
    """
    def __init__(self, choice_type, description, effect, condition=None):
        self.type = choice_type
        self.description = description
        self.effect = effect
        self.condition = condition

    def choose(self, player):
        """
        :type player: Player
        """
        player.states.update(self.effect.state_change)
        print(self.effect.text)


class ChoiceSlot:
    choices: List[Choice]

    def __init__(self):
        self.choices = []

    def add_choice(self, choice):
        """
        :type choice: Choice
        """
        self.choices.append(choice)

    def get_choice(self, player):
        i = 0
        while True:
            choice = self.choices[i]
            if choice.type is CHOICE_TYPE_IF and not choice.condition.items() <= player.states.items():
                i += 1
            else:
                return self.choices[i]

    def choose(self, player):
        """
        :type player: Player
        """
        choice = self.get_choice(player)
        choice.choose(player)
        if choice.type is not CHOICE_TYPE_PERMANENT:
            self.choices.remove(choice)


class Node:
    choice_slots: List[ChoiceSlot]

    def __init__(self, node_name):
        """
        :type node_name: str
        """
        self.node_name = node_name
        self.choice_slots = []


class Player:
    def __init__(self, name):
        """
        :type name: str
        """
        self.name = name
        self.states = {}


the_player = Player("Testo der Clown")
the_player.states["Nase"] = "Verstopft"

start_node = Node("Start")

choice_slot1 = ChoiceSlot()
choice_slot1.add_choice(Choice(CHOICE_TYPE_ONCE, "In der Nase bohren", Effect("Das war... nutzlos", {"Nase": "frei"}, "Start")))
choice_slot1.add_choice(Choice(CHOICE_TYPE_PERMANENT, "Warten", Effect("Und wieder verstopft", {"Nase": "verstopft"}, "Start")))
start_node.choice_slots.append(choice_slot1)

choice_slot2 = ChoiceSlot()
choice_slot2.add_choice(Choice(CHOICE_TYPE_IF, "Freuen", Effect("Hurra, eine freie Nase!", {}, "Start"), {"Nase": "frei"}))
choice_slot2.add_choice(Choice(CHOICE_TYPE_PERMANENT, "Weinen", Effect("Ich bin immer traurig", {}, "Start")))
start_node.choice_slots.append(choice_slot2)

print(start_node.choice_slots[1].get_choice(the_player).description)
start_node.choice_slots[1].choose(the_player)
print("Status Nase:" + the_player.states["Nase"])

print(start_node.choice_slots[0].get_choice(the_player).description)
start_node.choice_slots[0].choose(the_player)
print("Status Nase:" + the_player.states["Nase"])

print(start_node.choice_slots[1].get_choice(the_player).description)
start_node.choice_slots[1].choose(the_player)
print("Status Nase:" + the_player.states["Nase"])

print(start_node.choice_slots[0].get_choice(the_player).description)
start_node.choice_slots[0].choose(the_player)
print("Status Nase:" + the_player.states["Nase"])
