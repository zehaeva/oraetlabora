from enum import Enum
import cmd
import random


class Variants(Enum):
    irish = 1
    french = 2


class GameLength(Enum):
    long = 1
    short = 2


class Actions(Enum):
    clear_land = 1
    build = 2
    place_brother = 3
    place_prior = 4
    contract = 5
    buy_plot = 6


class FieldType(Enum):
    water = 1
    coast = 2
    plain = 3
    hillside = 4
    mountain = 5


class BuildLocation(Enum):
    water = 1
    coast = 2
    meadow = 3
    hillside = 4
    mountain = 5


class BuildingRound(Enum):
    setup = 0
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
        return self.__dict__ == other.__dict__

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
    def __init__(self, name='Empty', description='Place a Card here', victory_points=0, village_points=0, build_cost=list(), variants=[Variants.irish, Variants.french],
                 build_locations=[BuildLocation.coast, BuildLocation.meadow, BuildLocation.hillside], religious=False, start_round=list(), number_of_players=[4],
                 allowable_actions=[Actions.contract, Actions.place_brother, Actions.place_prior]):
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
        self.allowable_actions = allowable_actions

    def __repr__(self):
        return 'Card: {}'.format(self.name, self.description)

    def __str__(self):
        return '{}: {}'.format(self.name, self.description)

    def take_action(self, action):
        if action in self.allowable_actions:
            pass
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Buildings(dict):
    def __init__(self, variant, number_of_players):
        self['forest'] = Card('Forest', 'Take Forest', start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5], allowable_actions=[Actions.clear_land])
        self['peat bog'] = Card('Peat Bog', 'Take Peat', start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5], allowable_actions=[Actions.clear_land])
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
        self['colefactory'] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 3, 4])
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
        self['shanty town'] = Card(name='Shanty Town', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self['farming village'] = Card(name='Farming Village', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self['market town'] = Card(name='Market Town', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self['fishing village'] = Card(name='Fishing Village', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self['artists colony'] = Card(name='Artists Colony', start_round=[BuildingRound.a], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self['hamlet'] = Card(name='Hamlet', start_round=[BuildingRound.b], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self['village'] = Card(name='Village', start_round=[BuildingRound.c], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self['hilltop village'] = Card(name='Hilltop Village', start_round=[BuildingRound.d], number_of_players=[1, 2, 3, 4], allowable_actions=[])

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

    def take(self, building_name):
        my_return = None
        if self[building_name] is not None:
            my_return = self[building_name]
            self[building_name] = None
        return my_return


class FieldSpot:
    def __init__(self, x, y, filed_type, card):
        self.x = x
        self.y = y
        self.filed_type = filed_type
        self.card = card


class PlayField:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        # I'm not sure I like this structure, I'm going to go with a list where each element has an x, y, type, and card spot

        self.field = list(list({'building': Card()} for j in range(width)) for i in range(height))
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
        self.setup(card=Card(allowable_actions=[Actions.build]), x=0, y=3, field=FieldType.plain)
        self.setup(card=Card(allowable_actions=[Actions.build]), x=1, y=3, field=FieldType.plain)

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
        self.turn_number = 0

    def available_actions(self, action):
        if action == Actions.clear_land:
            print('Select Land to clear:')
            loc_x = 0
        elif action == Actions.build:
            print('Select plot to build on:')
            loc_x = 0
        for x in self.land:
            loc_x += 1
            loc_y = 0
            for y in x:
                loc_y += 1
                if action in y['building'].allowable_actions:
                    print('{} @ {} x {}'.format(y['building'].name, loc_y, loc_x))
        pass

    def build(self, building, loc_x, loc_y):
        # check to see if space is blank

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


class RondelProgression:
    def __init__(self):
        self.progression = {1: {GameLength.long: {},
                                GameLength.short: {}},
                            2: {GameLength.long: {'turns': 25, 'a': 6, 'b': 11, 'c': 15, 'd': 20, 'e': 25, 'grape': 8, 'stone': 13, 'wheel': [0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]},
                                GameLength.short: {}},
                            3: {GameLength.long: {'turns': 25, 'a': 6, 'b': 11, 'c': 15, 'd': 20, 'e': 25, 'grape': 8, 'stone': 13, 'wheel': [0, 1, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]},
                                GameLength.short: {}},
                            4: {GameLength.long: {'turns': 25, 'a': 7, 'b': 10, 'c': 16, 'd': 19, 'e': 25, 'grape': 8, 'stone': 13, 'wheel': [0]},
                                GameLength.short: {},}
                            }


class Rondel:
    def __init__(self, variant=Variants.irish, number_of_players=3, length=GameLength.long):
        rp = RondelProgression()
        self.setup = rp.progression[number_of_players][length]
        self.current_turn = 0
        self.current_player = 0
        self.variant = variant
        self.wheel = []
        for i in self.setup['wheel']:
            self.wheel.append(WheelSpace(i))

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


class Game:
    def __init__(self):
        self.players = None
        self.rondel = None
        self.resources = None
        self.buildings = None
        self.variant = None


# set up the Resources
resources = Resources()


class OraetLaboraShell(cmd.Cmd):
    intro = 'Welcome to Ora et Labora! Type help or ? to list commands.\n'
    prompt = '(O&L) '
    min_players = 1
    max_players = 4
    variant = None
    players = list()
    resources = Resources()
    buildings = None
    rondel = None
    current_game_length = None
    current_game_phase = BuildingRound.setup

    # basic commands
    def do_variant(self, arg):
        ''' display current variant '''
        if self.variant == Variants.irish:
            print("Irish")
        elif self.variant == Variants.french:
            print("French")
        else:
            print("Variant Not Set")

    def do_setvariant(self, arg):
        ''' set which variant is being used, Irish or French '''
        if self.current_game_phase is BuildingRound.setup:
            if self.variant is None:
                if arg == 1 or arg == '1' or arg.lower() == 'irish':
                    print('setting Variant to Irish')
                    self.variant = Variants.irish
                else:
                    print('setting Variant to French')
                    self.variant = Variants.french
        else:
            print("Sorry, we're not in the setup phase!")

    def do_player(self, arg):
        ''' display all players or just one player if you provide a name '''
        for player in self.players:
            if arg.lower() == player.name:
                print(player)

    def do_addplayer(self, arg):
        ''' add player to a game '''
        if self.current_game_phase == BuildingRound.setup:
            if len(self.players) == self.max_players:
                print('You have the maximum amount of players!')
            else:
                if self.variant is None:
                    print('You have to set the variant first!')
                else:
                    self.players.append(Player(arg, self.variant))
                    print('added player ({}) {}'.format(len(self.players), arg))

    def do_removeplayer(self, arg):
        ''' Remove player from the game '''
        if self.current_game_phase == BuildingRound.setup:
            if len(self.players) == 0:
                print("there's no one to remove!")
            else:
                pass

    def do_setlength(self, arg):
        ''' sets the length of the game, Short or Long '''
        if self.current_game_phase == BuildingRound.setup:
            if arg == 1 or arg == '1' or arg.lower() == 'long':
                print("Game Length set to Long")
                self.current_game_length = GameLength.long
            else:
                print("Game Length set to Short")
                self.current_game_length = GameLength.short

    def do_start(self, arg):
        ''' starts the game '''
        if self.variant is not None:
            if self.min_players <= len(self.players) <= self.max_players:
                if self.current_game_length is not None:
                    # set up rondel
                    self.rondel = Rondel(variant=self.variant, number_of_players=len(self.players), length=self.current_game_length)
                    # set up available buildings
                    self.buildings = Buildings(self.variant, len(self.players))
                    # randomize turn order
                    random.shuffle(self.players)

                    print('Starting a new game of Ora et Labora!')
                    print('Variant: {}'.format(self.variant))
                    print('Length: {}'.format(self.current_game_length))
                    print('Turn order:')
                    j = 1
                    for i in self.players:
                        print("({}) {}".format(j, i.name))
                        j += 1

                    # change prompt
                    self.prompt = "(O&L) Turn {}: {}:".format(self.rondel.current_turn, self.players[self.rondel.current_player].name)
                    self.current_game_phase = BuildingRound.start
                else:
                    print("You have to set the game length before you can start!")
            else:
                print("You need at least {}, and no more than {}, players to play!".format(self.min_players, self.max_players))
        else:
            print("You have to set the variant for you start!")


def parse(arg):
    ''' Convert a series of zero or more numbers to an argument tuple '''
    return tuple(map(int, arg.split()))


if __name__ == '__main__':
    OraetLaboraShell().cmdloop()

'''
# choose the variant
variant = Variants.irish

# choose game length
current_game_length = GameLength.long

players = list()
# enter the players
players.append(Player('Howard', variant))
players.append(Player('Andrew', variant))
players.append(Player('Chris', variant))

# set up the rondel buildings used
rondel = Rondel(variant=variant, number_of_players=len(players), length=current_game_length)
buildings = Buildings(variant, len(players))

print(buildings.a().values())

print(rondel)

print(players[0].land)
for value in players[0].resources.values():
    print('({}) {}'.format(value.quantity, value))

players[0].available_actions(Actions.clear_land)
players[0].available_actions(Actions.build)
'''
