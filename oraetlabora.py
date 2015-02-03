from enum import Enum


class Variants(Enum):
    irish = 1
    french = 2


class Actions(Enum):
    clear_land = 1
    build = 2
    place_brother = 3
    place_prior = 4
    contract = 5


class BuildLocation(Enum):
    water = 1
    coast = 2
    meadow = 3
    hillside = 4
    mountain = 5


class BuildingRound(Enum):
    start = 1
    a = 2
    b = 3
    c = 4
    d = 5
    e = 6


class Resource:
    def __init__(self, name='', description='', basic=False, food_value=0, fuel_value=0.0, currency_value=0, victory_points=0.0, variants=[Variants.irish, Variants.french],
                 start_turn=0, token=False):
        self.name = name
        self.description = description
        self.basic = basic
        self.food_value = food_value
        self.fuel_value = fuel_value
        self.currency_value = currency_value
        self.victory_points = victory_points
        self.variants = variants
        self.start_turn = start_turn
        self.token = token
        self.quantity = 0

    def __repr__(self):
        return '({}) {}'.format(self.quantity, self.name)

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
        return self


class Resources(dict):
    def __init__(self):
        self['wood'] = Resource(name='Wood', fuel_value=1, basic=True, token=True)
        self['wheat'] = Resource(name='Wheat', food_value=1, basic=True, token=True)
        self['clay'] = Resource(name='Clay', basic=True, token=True)
        self['coin'] = Resource(name='Coin', food_value=1, currency_value=1, basic=True, victory_points=0.2, token=True)
        self['sheep'] = Resource(name='Sheep', food_value=2, basic=True, token=True)
        self['peat'] = Resource(name='Peat', fuel_value=2, basic=True, token=True)

        self['straw'] = Resource(name='Straw', fuel_value=.05)
        self['coal'] = Resource(name='Coal', fuel_value=3)
        self['ceramic'] = Resource(name='Ceramic', victory_points=3)
        self['whiskey'] = Resource(name='Whiskey', food_value=2, currency_value=2, victory_points=1, variants=[Variants.irish])
        self['stone'] = Resource(name='Stone', token=True)
        self['ornament'] = Resource(name='Ornament', victory_points=4)
        self['reliquary'] = Resource(name='Reliquary', victory_points=8)
        self['grape'] = Resource(name='Grape', food_value=1, variants=[Variants.french], token=True)
        self['wine'] = Resource(name='Wine', food_value=1, currency_value=1, victory_points=1, variants=[Variants.french])
        self['flour'] = Resource(name='Flour', food_value=1, variants=[Variants.french])
        self['bread'] = Resource(name='Bread', food_value=5, variants=[Variants.french])
        self['malt'] = Resource(name='Malt', food_value=1, variants=[Variants.irish])
        self['beer'] = Resource(name='Beer', food_value=5, variants=[Variants.irish])
        self['book'] = Resource(name='Book', victory_points=2)
        self['meat'] = Resource(name='Meat', food_value=5)

    def basic(self, quantity=0):
        my_return = {}
        for key in self:
            if self[key].basic:
                my_return[key] = self[key].set_quantity(quantity)
        return my_return


class Brother:
    def __init__(self):
        self.x = -100
        self.y = -100


class Prior(Brother):
    pass


class Card:
    def __init__(self, name='Empty', description='Place a Card here', victory_points=0, village_points=0, build_cost=[], variants=[Variants.irish, Variants.french],
                 build_locations=[BuildLocation.coast, BuildLocation.meadow, BuildLocation.hillside], religious=False, start_round=[], number_of_players=[4]):
        self.name = name
        self.description = description
        self.victory_points = victory_points
        self.village_points = village_points
        self.build_cost = build_cost
        self.variants = variants
        self.build_locations = build_locations
        self.religious = religious
        self.start_round = start_round
        self.number_of_players = number_of_players

    def __repr__(self):
        return 'Card: {}'.format(self.name, self.description)

    def __str__(self):
        return '{}: {}'.format(self.name, self.description)

    def action(self):
        pass


class Buildings(dict):
    def __init__(self, variant, number_of_players):
        self['forest'] = Card('Forest', 'Take Forest', start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5])
        self['peat bog'] = Card('Peat Bog', 'Take Peat', start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5])
        self['clay mound'] = Card('Clay Mound', 'Take Clay', 3, start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5])
        self['cloister office'] = Card('Cloister Office', 'Take Gold', 2, start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5])
        self['farm yard'] = Card('Farm Yard', 'Take Straw or Take Sheep', 2, start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5])

    #   Start Buildings
        self['brewery'] = Card('Brewery', '1 malt, 1 grain -> 1 beer and then/or 1 beer -1x-> 7 coins', victory_points=9, village_points=7, variants=[Variants.irish],
                               build_cost=[resources['stone'].set_quantity(2), resources['straw'].set_quantity(1)], start_round=[BuildingRound.start],
                               number_of_players=[1, 2, 3, 4])
        self['cloister courtyard'] = Card('Cloister Courtyard', '3 different goods -1x-> 6 identical basic goods', victory_points=4, village_points=4,
                                          build_cost=[resources['wood'].set_quantity(2)], start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self['priory'] = Card(start_round=[BuildingRound.start], number_of_players=[1, 3, 4])
        self['grain storage'] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 4])
        self['granary'] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 4])
        self['windmill'] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['malthouse'] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['bakery'] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['fuel merchant'] = Card(start_round=[BuildingRound.start], number_of_players=[1, 3, 4])
        self['peat coal kiln'] = Card(start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self['market'] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['false lighthouse'] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['cloister garden'] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 3, 4])
        self['spinning mill'] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self['carpentry'] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[4])
        self['cottage'] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 4])
        self['houseboat'] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['harbor promenade'] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['stone merchant'] = Card(start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self['builders` market'] = Card(start_round=[BuildingRound.start], number_of_players=[1, 4])
    #   A Buildings
        self['grapevine'] = Card(name='Grapevine', start_round=[BuildingRound.a, BuildingRound.c], variants=[Variants.french], number_of_players=[2, 3, 4])
        self['sacred site'] = Card(name='Sacred Site', start_round=[BuildingRound.a], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['financed estate'] = Card(name='Financed Estate', start_round=[BuildingRound.a], variants=[Variants.french], number_of_players=[1, 4])
        self['druids house'] = Card(name='Druids House', start_round=[BuildingRound.a], variants=[Variants.irish], number_of_players=[1, 4])
        self['cloister chapter house'] = Card(name='Cloister Chapter House', start_round=[BuildingRound.a], number_of_players=[1, 3, 4])
        self['cloister library'] = Card(name='Cloister Library', start_round=[BuildingRound.a], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['scriptorium'] = Card(name='Scriptorium', start_round=[BuildingRound.a], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['cloister workshop'] = Card(name='Cloister Workshop', start_round=[BuildingRound.a], number_of_players=[1, 2, 3, 4])
        self['slaughterhouse'] = Card(name='Slaughterhouse', start_round=[BuildingRound.a], number_of_players=[1, 2, 3, 4])
    #   B Buildings
        self['inn'] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 3, 4])
        self['alehouse'] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self['winery'] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['whiskey distillery'] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['quarry'] = Card(start_round=[BuildingRound.b], number_of_players=[1, 2, 3, 4])
        self['bathhouse'] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 4])
        self['locutory'] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 4])
        self['cloister church'] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['chapel'] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['chamber of wonders'] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 4])
        self['portico'] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 4])
        self['shipyard'] = Card(start_round=[BuildingRound.b], number_of_players=[1, 2, 3, 4])
    #   C Buildings
        self['palace'] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['grand manor'] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['castle'] = Card(start_round=[BuildingRound.c], number_of_players=[1, 2, 3, 4])
        self['c-quarry'] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[3, 4])
        self['forest hut'] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self['town estate'] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['refectory'] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['c-grapevine'] = Card(start_round=[BuildingRound.c], number_of_players=[4])
        self['coal harbor'] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 4])
        self['calefactory'] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 3, 4])
        self['filial church'] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self['shipping company'] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['cooperage'] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
    #   D Buildings
        self['sacristy'] = Card(start_round=[BuildingRound.d], number_of_players=[1, 2, 3, 4])
        self['forgers workshop'] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['round tower'] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['pilgrimage site'] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 3, 4])
        self['camera'] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self['dormitory'] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['bulwark'] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['printing office'] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self['festival ground'] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self['estate'] = Card(start_round=[BuildingRound.d], number_of_players=[1, 4])
        self['hospice'] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 3, 4])
        self['guesthouse'] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self['house of the brotherhood'] = Card(start_round=[BuildingRound.d], number_of_players=[1, 2, 3, 4])
    #   settlements
        self['shanty town'] = Card(name='Shanty Town', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self['farming village'] = Card(name='Farming Village', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self['market town'] = Card(name='Market Town', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self['fishing village'] = Card(name='Fishing Village', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self['artists colony'] = Card(name='Artists Colony', start_round=[BuildingRound.a], number_of_players=[1, 2, 3, 4])
        self['hamlet'] = Card(name='Hamlet', start_round=[BuildingRound.b], number_of_players=[1, 2, 3, 4])
        self['village'] = Card(name='Village', start_round=[BuildingRound.c], number_of_players=[1, 2, 3, 4])
        self['hilltop village'] = Card(name='Hilltop Village', start_round=[BuildingRound.d], number_of_players=[1, 2, 3, 4])

        self.variant = variant
        self.number_of_players = number_of_players

    def round_list(self, building_round):
        my_return = {}
        for key in self:
            if building_round in self[key].start_round and self.variant in self[key].variants and self.number_of_players in self[key].number_of_players:
                my_return[key] = self[key]
        return my_return

    def start(self):
        return self.round_list(BuildingRound.start)

    def a(self):
        return self.round_list(BuildingRound.a)

    def b(self):
        return self.round_list(BuildingRound.b)

    def c(self):
        return self.round_list(BuildingRound.c)

    def d(self):
        return self.round_list(BuildingRound.d)


class FieldType(Enum):
    water = 1
    coast = 2
    plain = 3
    hillside = 4
    mountain = 5


class PlayField:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.field = list(list({'building': Card()} for i in range(width)) for i in range(height))
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
                my_return = '{} | {}: {}'.format(my_return, y['type'].name, y['building'])
            my_return = "{} |\n".format(my_return)
        return my_return

    def add_card(self, x, y, card):
        self.field[x][y]['building'] = card

    def setup(self, x, y, card, field):
        self.field[x][y]['building'] = card
        self.field[x][y]['type'] = field

    def remove_card(self, x, y):
        self.field[x][y] = Card()

    def __iter__(self):
        return iter(self.field)

    def __len__(self):
        return len(self.field)


class StartField(PlayField):
    def __init__(self, buildings):
        PlayField.__init__(self, 2, 5)
        self.setup(card=buildings['forest'], x=0, y=1, field=FieldType.plain)
        self.setup(card=buildings['forest'], x=0, y=2, field=FieldType.plain)
        self.setup(card=buildings['forest'], x=1, y=1, field=FieldType.plain)
        self.setup(card=buildings['peat bog'], x=0, y=0, field=FieldType.plain)
        self.setup(card=buildings['peat bog'], x=1, y=0, field=FieldType.plain)
        self.setup(card=buildings['cloister office'], x=1, y=4, field=FieldType.plain)
        self.setup(card=buildings['clay mound'], x=0, y=4, field=FieldType.plain)
        self.setup(card=buildings['farm yard'], x=1, y=2, field=FieldType.plain)
        self.setup(card=Card(), x=0, y=3, field=FieldType.plain)
        self.setup(card=Card(), x=1, y=3, field=FieldType.plain)

    def __str__(self):
        return PlayField.__str__(self)


class Coast(PlayField):
    def __init__(self):
        PlayField.__init__(self, 2, 2)


class PlayerResources:
    def __init__(self, resources):
        self.resources = resources

    def __repr__(self):
        return self.resources

    def victory_points(self):
        tally = 0
        for resource in self.resources:
            tally += resource.total_victory_points()
        return tally

    def add(self, resource):
        found = False
        for item in self.resources:
            if resource == item:
                item.quantity += resource.quantity
                found = True
        if not found:
            self.resources.append(resource)

    def fuel(self):
        tally = 0
        for resource in self.resources:
            tally += resource.total_fuel()
        return tally

    def currency(self):
        tally = 0
        for resource in self.resources:
            tally += resource.total_currency()
        return tally


class Player:
    def __init__(self, name, variant):
        self.name = name
        self.land = StartField(Buildings(variant=variant, number_of_players=0))
        self.clergy = [Brother(), Brother(), Prior()]
        self.resources = Resources().basic(quantity=1)

    def take_action(self, action):
        if action == Actions.clear_land:
            print('Select Land to clear:')
            loc_x = 0
            for x in self.land:
                loc_x += 1
                loc_y = 0
                for y in x:
                    loc_y += 1
                    if 'forest' in y['building'].name.lower():
                        print('Forest @ {} x {}'.format(loc_y, loc_x))
                    elif 'peat' in y['building'].name.lower():
                        print('Peat Bog @ {} x {}'.format(loc_y, loc_x))
        pass

    def build(self):
        pass

    def tally_fuel(self, ):
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

        print('Player {player_name} took {resource_quantity} {resource_name}'.format(player_name=self.name, resource_quantity=resource.quantity, resource_name=resource.name))

    def tally_resource_victory_points(self):
        tally = 0
        for resource in self.resources:
            tally += resource.total_victory_points()
        return tally


class WheelSpace:
    def __init__(self, value):
        self.value = value
        self.resources = []

    def __repr__(self):
        return 'Resources {}'.format(self.resources)


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
            if self.variant in temp[key].variants and temp[key].token:
                self.wheel[0].resources.append(temp[key])
        self.wheel[0].resources.append(Resource(name='Joker', token=True))

    def next_turn(self):
        self.current_turn += 1
        for i in range(13, 0, -1):
            for space_resources in self.wheel[i-1].resources:
                self.wheel[i].resources.append(space_resources.set_quantity(self.wheel[i].value))
            self.wheel[i-1].resources.clear()

    def take_resource(self, player, resource):
        for i in range(14, 0, -1):
            for wheel_resource in self.wheel[i-1].resources:
                if resource == wheel_resource:
                    self.wheel[i-1].resources.remove(wheel_resource)
                    player.add_resource(wheel_resource)
                    self.wheel[0].resources.append(wheel_resource.set_quantity(0))
                    break

    def __repr__(self):
        return "Rondel:\nCurrentTurn {}\n{}".format(self.current_turn, self.wheel)


class RondelProgression:
    def __init__(self, number_of_players):
        self.progression = {'1': {'long': {}, 'short': {}},
                            '2': {'long': {}, 'short': {}},
                            '3': {'long': {'turns': 25, 'a': 6, 'b': 11, 'c': 15, 'd': 20, 'e': 25, 'grape': 8, 'stone': 13}, 'short': {}},
                            '4': {'long': {'turns': 25, 'a': 7, 'b': 10, 'c': 16, 'd': 19, 'e': 25, 'grape': 8, 'stone': 13}, 'short': {}}}
        self.progression.append([])

variant = Variants.irish

rondel = Rondel(variant)
resources = Resources()
buildings = Buildings(variant, 3)

print(buildings.a().values())

players = list()
players.append(Player('Howard', variant))
players.append(Player('Andrew', variant))
players.append(Player('Chris', variant))

print(rondel)

print(players[0].land)
for value in players[0].resources.values():
    print('({}) {}'.format(value.quantity, value))

players[0].take_action(Actions.clear_land)