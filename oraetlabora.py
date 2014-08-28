class Player:
    def __init__(self, name):
        self.name = name
        self.land = StartField()
        self.clergy = [Brother(), Brother(), Prior()]

    def take_action(self, ):
        pass


class Brother:
    def __init__(self):
        self.x = -100
        self.y = -100


class Prior(Brother):
    pass


class Card:
    def __init__(self, name='Empty', description='Place a Card here', victory_points=0, village_points=0, build_cost={}):
        self.name = name
        self.description = description
        self.victory_points = victory_points
        self.village_points = village_points
        self.build_cost = build_cost
        self.build_locations = []

    def __str__(self):
        return '{}: {}'.format(self.name, self.description)

    def action(self):
        pass


class Buildings(dict):
    def __init__(self):
        self['Forest'] = Card('Forest', 'Take Forest')
        self['Peat Bog'] = Card('Peat Bog', 'Take Peat')
        self['Clay Mound'] = Card('Clay Mound', 'Take Clay', 3)
        self['Cloister Office'] = Card('Cloister Office', 'Take Gold', 2)
        self['Farm Yard'] = Card('Farm Yard', 'Take Straw or Take Sheep', 2)


class Forest(Card):
    def __init__(self):
        self.name = 'Forest'
        self.description = 'Take Forest'


class PeatBog(Card):
    def __init__(self):
        self.name = 'Peat Bog'
        self.description = 'Take Peat'


class ClayMound(Card):
    def __init__(self):
        self.name = 'Clay Mound'
        self.description = 'Take Clay'
        self.village_points = 3


class CloisterOffice(Card):
    def __init__(self):
        self.name = 'Cloister Office'
        self.description = 'Take Gold'
        self.village_points = 2


class FarmYard(Card):
    def __init__(self):
        self.name = 'Farm Yard'
        self.description = 'Take Straw or Take Sheep'
        self.village_points = 2


class Resource:
    def __init__(self, name='', description=''):
        self.name = name
        self.description = description


class PlayField:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = list(list(Card() for i in range(width)) for i in range(height))
        # self.size_field()

    def size_field(self):
        for x in range(self.width):
            self.field.append([])
        for y in range(self.height):
            self.field[x].append(Card())

    def __str__(self):
        my_return = ''
        for x in self.field:
            for y in x:
                my_return = '{} | {}'.format(my_return, y)
            my_return = "{} |\n".format(my_return)
        return my_return

    def add_card(self, x, y, card):
        self.field[x][y] = card

    def remove_card(self, x, y):
        self.field[x][y] = Card()


class StartField(PlayField):
    def __init__(self):
        PlayField.__init__(self, 2, 5)
        self.add_card(card=Forest(), x=0, y=1)
        self.add_card(card=Forest(), x=0, y=2)
        self.add_card(card=Forest(), x=1, y=1)
        self.add_card(card=PeatBog(), x=0, y=0)
        self.add_card(card=PeatBog(), x=1, y=0)
        self.add_card(card=CloisterOffice(), x=1, y=4)
        self.add_card(card=ClayMound(), x=0, y=4)
        self.add_card(card=FarmYard(), x=1, y=2)

    def __str__(self):
        return PlayField.__str__(self)


class Action:
    def __init__(self):
        pass


class WheelSpace:
    def __init__(self, value):
        self.value = value
        self.resources = []


class Rondel:
    def __init__(self):
        self.current_turn = 0
        self.wheel = []
        self.wheel.append(WheelSpace(0))
        self.wheel.append(WheelSpace(1))
        self.wheel.append(WheelSpace(2))
        self.wheel.append(WheelSpace(3))
        self.wheel.append(WheelSpace(4))
        self.wheel.append(WheelSpace(5))
        self.wheel.append(WheelSpace(6))
        self.wheel.append(WheelSpace(6))
        self.wheel.append(WheelSpace(7))
        self.wheel.append(WheelSpace(7))
        self.wheel.append(WheelSpace(8))
        self.wheel.append(WheelSpace(8))
        self.wheel.append(WheelSpace(9))
        self.wheel.append(WheelSpace(10))

    def next_turn(self):
        self.current_turn += 1


class RondelProgression:
    def __init__(self, number_of_players):
        self.progression = {'1': {'long': [], 'short': []},
                            '2': {'long': [], 'short': []},
                            '3': {'long': [], 'short': []},
                            '4': {'long': [], 'short': []}}
        self.progression.append([])

players = list()
players.append(Player('Howard'))

print(players[0].land)
