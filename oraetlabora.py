from enum import Enum
import cmd
import random


class Variants(Enum):
    irish = 1
    french = 2


class GameLength(Enum):
    long = 1
    short = 2


def clear_peat(rondel, player):
    return rondel.take_resource(player=player, resource=resources['peat'])


class Actions(Enum):
    clear_land = 0
    clear_peat = 1
    clear_wood = 2
    build = 3
    place_brother = 4
    place_prior = 5
    contract = 6
    buy_plot = 7


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


class Building(Enum):
    forest = 0
    peat_bog = 1
    clay_mound = 2
    cloister_office = 3
    farm_yard = 4
    brewery = 5
    cloister_courtyard = 6
    priory = 7
    grain_storage = 8
    granary = 9
    windmill = 10
    malthouse = 11
    bakery = 12
    fuel_merchant = 13
    peat_coal_kiln = 14
    market = 15
    false_lighthouse = 16
    cloister_garden = 17
    spinning_mill = 18
    carpentry = 19
    cottage = 20
    houseboat = 21
    harbor_promenade = 22
    stone_merchant = 23
    builders_market = 24
    grapevine = 25
    sacred_site = 26
    financed_estate = 27
    druids_house = 28
    cloister_chapter_house = 29
    cloister_library = 30
    scriptorium = 31
    cloister_workshop = 32
    slaughterhouse = 33
#   B Buildings
    inn = 34
    alehouse = 35
    winery = 36
    whiskey_distillery = 37
    quarry = 38
    bathhouse = 39
    locutory = 40
    cloister_church = 41
    chapel = 42
    chamber_of_wonders = 43
    portico = 44
    shipyard = 45
#   C Buildings
    palace = 46
    grand_manor = 47
    castle = 48
    c_quarry = 49
    forest_hut = 50
    town_estate = 51
    refectory = 52
    c_grapevine = 53
    coal_harbor = 54
    colefactory = 55
    filial_church = 56
    shipping_company = 57
    cooperage = 58
#   D Buildings
    sacristy = 59
    forgers_workshop = 60
    round_tower = 61
    pilgrimage_site = 62
    camera = 63
    dormitory = 64
    bulwark = 65
    printing_office = 66
    festival_ground = 67
    estate = 68
    hospice = 69
    guesthouse = 70
    house_of_the_brotherhood = 71
#   settlements
    shanty_town = 72
    farming_village = 73
    market_town = 74
    fishing_village = 75
    artists_colony = 76
    hamlet = 77
    village = 78
    hilltop_village = 79


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
        if isinstance(other, str):
            return self.name == other
        else:
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

    def take_action(self, action, rondel):
        if action in self.allowable_actions:
            if action is Actions.place_brother:
                pass
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__


class Buildings(dict):
    def __init__(self, variant, number_of_players):
        self[Building.forest] = Card('Forest', 'Take Forest', start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5], allowable_actions=[Actions.clear_land])
        self[Building.peat_bog] = Card('Peat Bog', 'Take Peat', start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5], allowable_actions=[Actions.clear_land])
        self[Building.clay_mound] = Card('Clay Mound', 'Take Clay', 3, start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5],
                                         allowable_actions=[Actions.place_brother, Actions.place_prior])
        self[Building.cloister_office] = Card('Cloister Office', 'Take Gold', 2, start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5])
        self[Building.farm_yard] = Card('Farm Yard', 'Take Straw or Take Sheep', 2, start_round=[BuildingRound.start], number_of_players=[0, 1, 2, 3, 4, 5])

    #   Start Buildings
        self[Building.brewery] = Card('Brewery', '1 malt, 1 grain -> 1 beer and then/or 1 beer -1x-> 7 coins', victory_points=9, village_points=7, variants=[Variants.irish],
                                      build_cost=[resources['stone'].set_quantity(2), resources['straw'].set_quantity(1)], start_round=[BuildingRound.start],
                                      number_of_players=[1, 2, 3, 4])
        self[Building.cloister_courtyard] = Card('Cloister Courtyard', '3 different goods -1x-> 6 identical basic goods', victory_points=4, village_points=4,
                                                 build_cost=[resources['wood'].set_quantity(2)], start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self[Building.priory] = Card(start_round=[BuildingRound.start], number_of_players=[1, 3, 4])
        self[Building.grain_storage] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 4])
        self[Building.granary] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 4])
        self[Building.windmill] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.malthouse] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.bakery] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.fuel_merchant] = Card(start_round=[BuildingRound.start], number_of_players=[1, 3, 4])
        self[Building.peat_coal_kiln] = Card(start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self[Building.market] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.false_lighthouse] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.cloister_garden] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 3, 4])
        self[Building.spinning_mill] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self[Building.carpentry] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[4])
        self[Building.cottage] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 4])
        self[Building.houseboat] = Card(start_round=[BuildingRound.start], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.harbor_promenade] = Card(start_round=[BuildingRound.start], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.stone_merchant] = Card(start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4])
        self[Building.builders_market] = Card(start_round=[BuildingRound.start], number_of_players=[1, 4])
    #   A Buildings
        self[Building.grapevine] = Card(name='Grapevine', start_round=[BuildingRound.a, BuildingRound.c], variants=[Variants.french], number_of_players=[2, 3, 4])
        self[Building.sacred_site] = Card(name='Sacred Site', start_round=[BuildingRound.a], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.financed_estate] = Card(name='Financed Estate', start_round=[BuildingRound.a], variants=[Variants.french], number_of_players=[1, 4])
        self[Building.druids_house] = Card(name='Druids House', start_round=[BuildingRound.a], variants=[Variants.irish], number_of_players=[1, 4])
        self[Building.cloister_chapter_house] = Card(name='Cloister Chapter House', start_round=[BuildingRound.a], number_of_players=[1, 3, 4])
        self[Building.cloister_library] = Card(name='Cloister Library', start_round=[BuildingRound.a], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.scriptorium] = Card(name='Scriptorium', start_round=[BuildingRound.a], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.cloister_workshop] = Card(name='Cloister Workshop', start_round=[BuildingRound.a], number_of_players=[1, 2, 3, 4])
        self[Building.slaughterhouse] = Card(name='Slaughterhouse', start_round=[BuildingRound.a], number_of_players=[1, 2, 3, 4])
    #   B Buildings
        self[Building.inn] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 3, 4])
        self[Building.alehouse] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self[Building.winery] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.whiskey_distillery] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.quarry] = Card(start_round=[BuildingRound.b], number_of_players=[1, 2, 3, 4])
        self[Building.bathhouse] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 4])
        self[Building.locutory] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 4])
        self[Building.cloister_church] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.chapel] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.chamber_of_wonders] = Card(start_round=[BuildingRound.b], variants=[Variants.french], number_of_players=[1, 4])
        self[Building.portico] = Card(start_round=[BuildingRound.b], variants=[Variants.irish], number_of_players=[1, 4])
        self[Building.shipyard] = Card(start_round=[BuildingRound.b], number_of_players=[1, 2, 3, 4])
    #   C Buildings
        self[Building.palace] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.grand_manor] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.castle] = Card(start_round=[BuildingRound.c], number_of_players=[1, 2, 3, 4])
        self[Building.c_quarry] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[3, 4])
        self[Building.forest_hut] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self[Building.town_estate] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.refectory] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.c_grapevine] = Card(start_round=[BuildingRound.c], number_of_players=[4])
        self[Building.coal_harbor] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 4])
        self[Building.colefactory] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 3, 4])
        self[Building.filial_church] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self[Building.shipping_company] = Card(start_round=[BuildingRound.c], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.cooperage] = Card(start_round=[BuildingRound.c], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
    #   D Buildings
        self[Building.sacristy] = Card(start_round=[BuildingRound.d], number_of_players=[1, 2, 3, 4])
        self[Building.forgers_workshop] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.round_tower] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.pilgrimage_site] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 3, 4])
        self[Building.camera] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self[Building.dormitory] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.bulwark] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.printing_office] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 2, 3, 4])
        self[Building.festival_ground] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 2, 3, 4])
        self[Building.estate] = Card(start_round=[BuildingRound.d], number_of_players=[1, 4])
        self[Building.hospice] = Card(start_round=[BuildingRound.d], variants=[Variants.french], number_of_players=[1, 3, 4])
        self[Building.guesthouse] = Card(start_round=[BuildingRound.d], variants=[Variants.irish], number_of_players=[1, 3, 4])
        self[Building.house_of_the_brotherhood] = Card(start_round=[BuildingRound.d], number_of_players=[1, 2, 3, 4])
    #   settlements
        self[Building.shanty_town] = Card(name='Shanty Town', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self[Building.farming_village] = Card(name='Farming Village', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self[Building.market_town] = Card(name='Market Town', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self[Building.fishing_village] = Card(name='Fishing Village', start_round=[BuildingRound.start], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self[Building.artists_colony] = Card(name='Artists Colony', start_round=[BuildingRound.a], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self[Building.hamlet] = Card(name='Hamlet', start_round=[BuildingRound.b], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self[Building.village] = Card(name='Village', start_round=[BuildingRound.c], number_of_players=[1, 2, 3, 4], allowable_actions=[])
        self[Building.hilltop_village] = Card(name='Hilltop Village', start_round=[BuildingRound.d], number_of_players=[1, 2, 3, 4], allowable_actions=[])

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
        self.setup(card=buildings[Building.forest], x=0, y=1, field=FieldType.plain)
        self.setup(card=buildings[Building.forest], x=0, y=2, field=FieldType.plain)
        self.setup(card=buildings[Building.forest], x=1, y=1, field=FieldType.plain)
        self.setup(card=buildings[Building.peat_bog], x=0, y=0, field=FieldType.plain)
        self.setup(card=buildings[Building.peat_bog], x=1, y=0, field=FieldType.plain)
        self.setup(card=buildings[Building.cloister_office], x=1, y=4, field=FieldType.plain)
        self.setup(card=buildings[Building.clay_mound], x=0, y=4, field=FieldType.plain)
        self.setup(card=buildings[Building.farm_yard], x=1, y=2, field=FieldType.plain)
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
        # one and two players have really special rules, so I'm going to leave them out for a while
        self.progression = {1: {GameLength.long:  {'turns': 25, 'a': 6, 'b': 11, 'c': 15, 'd': 20, 'e': 25, 'grape': 11, 'stone': 18, 'wheel': [0, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]},
                                GameLength.short: {}},
                            2: {GameLength.long:  {'turns': 25, 'a': 6, 'b': 11, 'c': 15, 'd': 20, 'e': 25, 'grape': 11, 'stone': 18, 'wheel': [0, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]},
                                GameLength.short: {'turns': 25, 'a': 6, 'b': 11, 'c': 15, 'd': 20, 'e': 25, 'grape': 11, 'stone': 18, 'wheel': [0, 1, 2, 2, 3, 4, 4, 5, 6, 6, 7, 8, 10]}},
                            3: {GameLength.long:  {'turns': 25, 'a': 6, 'b': 11, 'c': 15, 'd': 20, 'e': 25, 'grape': 8,  'stone': 13, 'wheel': [0, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]},
                                GameLength.short: {'turns': 13, 'a': 3, 'b': 5,  'c': 7,  'd': 9,  'e': 13, 'grape': 4,  'stone': 6,  'wheel': [0, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]}},
                            4: {GameLength.long:  {'turns': 25, 'a': 7, 'b': 10, 'c': 16, 'd': 19, 'e': 25, 'grape': 8,  'stone': 13, 'wheel': [0, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]},
                                GameLength.short: {'turns': 13, 'a': 3, 'b': 5,  'c': 7,  'd': 9,  'e': 13, 'grape': 4,  'stone': 6,  'wheel': [0, 2, 3, 4, 5, 6, 6, 7, 7, 8, 8, 9, 10]}}
                            }


class Rondel:
    def __init__(self, variant=Variants.irish, number_of_players=3, length=GameLength.long):
        rp = RondelProgression()
        self.setup = rp.progression[number_of_players][length]
        self.current_turn = 0
        self.current_player_index = 0
        self.players = None
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
        for i in range(13, 0, -1):
            for wheel_resource in self.wheel[i-1].resources:
                if resource == wheel_resource:
                    self.wheel[i-1].resources.remove(wheel_resource)
                    player.add_resource(wheel_resource)
                    self.wheel[0].resources.append(wheel_resource.set_quantity(0))
                    break

    def current_player(self):
        if self.players is None:
            return self.current_player_index
        else:
            return self.players[self.current_player_index]

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
    min_players = 3
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
                    self.rondel.players = self.players
                    self.prompt = "(O&L) Turn {}: {}:".format(self.rondel.current_turn, self.rondel.current_player().name)
                    self.current_game_phase = BuildingRound.start
                else:
                    print("You have to set the game length before you can start!")
            else:
                print("You need at least {}, and no more than {}, players to play!".format(self.min_players, self.max_players))
        else:
            print("You have to set the variant for you start!")

    def do_autostart(self, arg):
        self.do_setvariant('irish')
        self.do_setlength('long')
        self.do_addplayer('howard')
        self.do_addplayer('jim')
        self.do_addplayer('andrew')
        self.do_start('')

    def do_action(self, arg):
        ''' clear x y: clears specified field
            brother x y: places lay brother at specified coordinate
            brother building: places lay brother at specified building
            prior x y: places prior at specified coordinate
            prior building: places prior at specified building
            contract player building: contract a player to use a building
            build building x y: build a building at the specified coordinates
            buy landscape x y: buy a landscape and place it at the specified coordinates
        '''
        if self.current_game_phase != BuildingRound.setup:
            args = arg.split()
            if 'brother' in args[0]:
                # check to see if the brother is available
                pass
            elif 'clear' in args[0]:
                # clear the land!
                if self.rondel.current_player().land.field[0][0]['building'] == self.buildings[Building.peat_bog]:
                    self.rondel.take_resource(self.rondel.current_player(), self.resources['peat'])
                    self.rondel.current_player().land.remove_card(0, 0)
                    print('{player_name} has cleared {resource_name} @ ({x},{y}) and received {resource_amount} {resource_name}'.format(self.rondel.current_player().name, 'peat', 0, 0, 0, 'peat'))
                    self.rondel.next_turn()
                    pass
            elif 'prior' in args[0]:
                # check to see if the prior is available first
                pass
            elif 'contract' in args[0]:
                pass
            elif 'build' in args[0]:
                pass
            elif 'buy' in args[0]:
                pass
            else:
                print("Sorry I don't recognize the command {}".format(args))


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
