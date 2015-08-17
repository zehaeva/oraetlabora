__author__ = 'zehaeva'

import unittest
import oraetlabora


class CardTest(unittest.TestCase):
    def setUp(self):
        self.card = oraetlabora.Card('Forest',
                                     'Take Forest',
                                     start_round=[oraetlabora.BuildingRound.start],
                                     number_of_players=[0, 1, 2, 3, 4],
                                     allowable_actions=[oraetlabora.Actions.clear_land],
                                     build_locations=[oraetlabora.BuildLocation.meadow])

    def test_name(self):
        self.assertTrue(self.card.name is 'Forest')

    def test_description(self):
        self.assertTrue(self.card.description == 'Take Forest')

    def test_start_round(self):
        self.assertTrue(oraetlabora.BuildingRound.start in self.card.start_round)
        self.assertFalse(oraetlabora.BuildingRound.a in self.card.start_round)
        self.assertFalse(oraetlabora.BuildingRound.b in self.card.start_round)
        self.assertFalse(oraetlabora.BuildingRound.c in self.card.start_round)
        self.assertFalse(oraetlabora.BuildingRound.d in self.card.start_round)

    def test_number_of_players(self):
        self.assertTrue(1 in self.card.number_of_players)
        self.assertTrue(2 in self.card.number_of_players)
        self.assertTrue(3 in self.card.number_of_players)
        self.assertTrue(4 in self.card.number_of_players)
        self.assertFalse(5 in self.card.number_of_players)

    def test_allowable_actions(self):
        self.assertTrue(oraetlabora.Actions.clear_land in self.card.allowable_actions)
        self.assertTrue(oraetlabora.Actions.build not in self.card.allowable_actions)

    def test_religious(self):
        self.assertTrue(self.card.religious is False)

    def test_victory_points(self):
        self.assertTrue(self.card.victory_points is 0)

    def test_village_points(self):
        self.assertTrue(self.card.village_points is 0)

    def test_build_locations(self):
        self.assertTrue(oraetlabora.BuildLocation.meadow in self.card.build_locations)
        self.assertFalse(oraetlabora.BuildLocation.coast in self.card.build_locations)
        self.assertFalse(oraetlabora.BuildLocation.hillside in self.card.build_locations)
        self.assertFalse(oraetlabora.BuildLocation.mountain in self.card.build_locations)
        self.assertFalse(oraetlabora.BuildLocation.water in self.card.build_locations)

    def test_variants(self):
        self.assertTrue(oraetlabora.Variants.irish in self.card.variants)
        self.assertTrue(oraetlabora.Variants.french in self.card.variants)


class FieldSpotTest(unittest.TestCase):
    def setUp(self):
        self.spot = oraetlabora.FieldSpot(x=2,
                                          y=3,
                                          filed_type=oraetlabora.FieldType.plain,
                                          card=oraetlabora.Card("Forest",
                                                                'Take Forest',
                                                                start_round=[oraetlabora.BuildingRound.start],
                                                                number_of_players=[0, 1, 2, 3, 4],
                                                                allowable_actions=[oraetlabora.Actions.clear_land],
                                                                build_locations=[oraetlabora.BuildLocation.meadow]))

    def test_x(self):
        self.assertTrue(self.spot.x is 2)
        self.assertTrue(self.spot.x == 2)
        self.assertTrue(self.spot.x is not 0)

    def test_y(self):
        self.assertTrue(self.spot.y is 3)
        self.assertTrue(self.spot.y == 3)
        self.assertTrue(self.spot.y is not 0)

    def test_field_type(self):
        self.assertTrue(self.spot.filed_type == oraetlabora.FieldType.plain)
        self.assertTrue(self.spot.filed_type is oraetlabora.FieldType.plain)
        self.assertTrue(self.spot.filed_type is not oraetlabora.FieldType.mountain)

class ResourceTest(unittest.TestCase):

    def setUp(self):
        self.resource = oraetlabora.Resource(name='Coin', food_value=1, currency_value=1, basic=True, victory_points=0.2, token=True)
        self.resource.quantity = 1

    def test_resource(self):
        self.assertTrue(self.resource.basic is True)
        self.assertTrue(self.resource.token is True)
        self.assertTrue(self.resource.name is 'Coin')
        self.assertTrue(self.resource.food_value is 1)

    def test_currency_value(self):
        self.assertTrue(self.resource.currency_value is 1)

    def test_quantity(self):
        self.assertTrue(self.resource.quantity is 1)

    def test_victory_points(self):
        self.assertTrue(self.resource.victory_points == 0.2)  # I hate floats

    def test_total_food(self):
        self.assertTrue(self.resource.total_food() is 1)

    def test_total_fuel(self):
        self.assertTrue(self.resource.total_fuel() == 0.0)

    def test_total_currency(self):
        self.assertTrue(self.resource.total_currency() is 1)

if __name__ == '__main__':
    unittest.main()
