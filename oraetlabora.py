from enum import Enum


class Player:
    def __init__(self, name):
        self.name = name
        self.land = StartField()
        self.clergy = [Brother(), Brother(), Prior()]
        self.resources = list()

        temp = Resources()
        for key in temp:
            if temp[key].basic:
                self.resources.append([temp[key], 1])

    def take_action(self, ):
        pass

    def add_resource(self, resource, quantity):
        success = False
        for value_pair in self.resources:
            if resource in value_pair:
                value_pair[1] += quantity
                success = True

        if not success:
            self.resources.append([resource, quantity])
            success = True

        if success:
            print('Player {player_name} took {resource_quantity} {resource_name}'.format(player_name=self.name, resource_quantity=quantity, resource_name=resource.name))


    def tally_fuel(self):
        tally = 0
        for resource in self.resources:
            tally += resource.total_fuel()
        return tally

    def tally_currency(self):
        tally = 0
        for resource in self.resources:
            tally += resource.total_currency()
        return tally

    def add_resource(self, resource):
        found = False
        for item in self.resources:
            if resource == item:
                item.quantity += resource.quantity
                found = True
        if not found:
            self.resources.append(resource)

    def tally_resource_victory_points(self):
        tally = 0
        for resource in self.resources:
            tally += resource.total_victory_points()
        return tally


class Brother:
    def __init__(self):
        self.x = -100
        self.y = -100


class Prior(Brother):
    pass


class Card:
    def __init__(self, name='Empty', description='Place a Card here', victory_points=0, village_points=0, build_cost=[], variation=[], build_location=[]):
        self.name = name
        self.description = description
        self.victory_points = victory_points
        self.village_points = village_points
        self.build_cost = build_cost
        self.variation = variation
        self.build_location = build_location
        self.build_locations = []

    def __repr__(self):
        return 'Card: {}'.format(self.name, self.description)

    def __str__(self):
        return '{}: {}'.format(self.name, self.description)

    def action(self):
        pass


class Buildings(dict):
    def __init__(self):
        irish = Variation(irish=True)
        french = Variation(french=True)
        self['Forest'] = Card('Forest', 'Take Forest', variation=[irish, french])
        self['Peat Bog'] = Card('Peat Bog', 'Take Peat', variation=[irish, french])
        self['Clay Mound'] = Card('Clay Mound', 'Take Clay', 3, variation=[irish, french])
        self['Cloister Office'] = Card('Cloister Office', 'Take Gold', 2, variation=[irish, french])
        self['Farm Yard'] = Card('Farm Yard', 'Take Straw or Take Sheep', 2, variation=[irish, french])

        self['Brewery'] = Card('Brewery', '1 malt, 1 grain -> 1 beer and then/or 1 beer -1x-> 7 coins', victory_points=9, village_points=7,
                               build_cost=[Resources['stone'].set_quantity(2), Resources['straw'].set_quantity(1)])
        self['Cloister Courtyard'] = Card('Cloister Courtyard', '3 different goods -1x-> 6 identical basic goods', victory_points=4, village_points=4,
                                          build_cost=[Resources['wood'].set_quantity(2)])


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


class Variants(Enum):
    irish = 1
    french = 2


class Resource:
    def __init__(self, name='', description='', basic=False, food_value=0, fuel_value=0.0, currency_value=0, victory_points=0.0, variants=[Variants.irish, Variants.french],
                 start_turn=0, tolken=False):
        self.name = name
        self.description = description
        self.basic = basic
        self.food_value = food_value
        self.fuel_value = fuel_value
        self.currency_value = currency_value
        self.victory_points = victory_points
        self.variants = variants
        self.start_turn = start_turn
        self.tolken = tolken

    def __repr__(self):
        return '{}'.format(self.name)

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other


    def total_food(self):
        return self.quantity * self.food_value

    def total_fuel(self):
        return self.quantity * self.fuel_value

    def total_currency(self):
        return self.quantity * self.currency_value

    def total_victory_points(self):
        return round(self.quantity * self.victory_points, 0)

    def set_quantity(self, quantity):
        self.quantity = quantity


class Resources(dict):
    def __init__(self):
        self['wood'] = Resource(name='Wood', fuel_value=1, basic=True)
        self['wheat'] = Resource(name='Wheat', food_value=1, basic=True)
        self['clay'] = Resource(name='Clay', basic=True)
        self['coin'] = Resource(name='Coin', food_value=1, currency_value=1, basic=True, victory_points=0.2)
        self['sheep'] = Resource(name='Sheep', food_value=2, basic=True)
        self['peat'] = Resource(name='Peat', fuel_value=2, basic=True)

        self['straw'] = Resource(name='Straw', fuel_value=.05)
        self['coal'] = Resource(name='Coal', fuel_value=3)
        self['ceramic'] = Resource(name='Ceramic', victory_points=3)
        self['whiskey'] = Resource(name='Whiskey', food_value=2, currency_value=2, victory_points=1, variants=[Variants.irish])
        self['stone'] = Resource(name='Stone', tolken=True)
        self['ornament'] = Resource(name='Ornament', victory_points=4)
        self['reliquary'] = Resource(name='Reliquary', victory_points=8)
        self['grape'] = Resource(name='Grape', food_value=1, variants=[Variants.french], tolken=True)
        self['wine'] = Resource(name='Wine', food_value=1, currency_value=1, victory_points=1, variants=[Variants.french])
        self['flour'] = Resource(name='Flour', food_value=1)
        self['bread'] = Resource(name='Bread', food_value=5)
        self['malt'] = Resource(name='Malt', food_value=1, variants=[Variants.irish])
        self['beer'] = Resource(name='Beer', food_value=5, variants=[Variants.irish])
        self['book'] = Resource(name='Book', victory_points=2)
        self['meat'] = Resource(name='Meat', food_value=5)


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


class Actions(Enum):
    take_resource = 1


class WheelSpace:
    def __init__(self, value):
        self.value = value
        self.resources = []

    def __repr__(self):
        return 'Resources {}, Amount {}'.format(self.resources, self.value)


class Rondel:
    def __init__(self, variant=Variants.irish):
        self.current_turn = 0
        self.variant = variant
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

        temp = Resources()
        for key in temp:
            if self.variant in temp[key].variants and temp[key].tolken:
                self.wheel[0].resources.append(temp[key])

    def next_turn(self):
        self.current_turn += 1
        for i in range(13, 0, -1):
            for space_resources in self.wheel[i-1].resources:
                self.wheel[i].resources.append(space_resources)
            self.wheel[i-1].resources.clear()

    def take_resource(self, player, resource):
        for i in range(14, 0, -1):
            if resource.name in self.wheel[i-1].resources:
                self.wheel[i-1].resources.remove(resource)
                self.wheel[0].resources.append(resource)
                player.add_resource(resource, self.wheel[i-1].value)
                break

    def __repr__(self):
        return "Rondel:\nCurrentTurn {}\n{}".format(self.current_turn, self.wheel)


class RondelProgression:
    def __init__(self, number_of_players):
        self.progression = {'1': {'long': [], 'short': []},
                            '2': {'long': [], 'short': []},
                            '3': {'long': [], 'short': []},
                            '4': {'long': [], 'short': []}}
        self.progression.append([])

rondel = Rondel(Variants.irish)
resources = Resources()

resources = Resources()

players = list()
players.append(Player('Howard'))

rondel.next_turn()
rondel.next_turn()
rondel.next_turn()
rondel.take_resource(players[0], resources['wood'])
print(rondel)
rondel.take_resource(players[0], resources['wood'])
rondel.next_turn()
print(rondel)

print(players[0].land)
for i in players[0].resources:
    print('({}) {}'.format(i, i.quantity))