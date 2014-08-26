class Card:
  def __init__(self, name = 'Empty', description = '', victory_points = 0, village_points = 0, build_cost = {}):
    self.name = name
    self.description = description
    self.victory_points = victory_points
    self.village_points = village_points
    self.build_cost = build_cost
    return None
  def __str__(self):
    return '{}: {}'.format(self.name, self.description)
  def action(self):
    pass

class Resource:
  def __init__(self, name = '', description = ''):
    self.name = ''
    self.description = ''

class Playfield:
    def __init__(self, height, width):
      self.field = []
      for x in range(width):
        self.field.append([])
        for y in range(height):
            self.field[x].append(Card())
    def __str__(self):
      myreturn = ''
      for x in self.field:
        for y in x:
          myreturn = '{} | {}'.format(myreturn, y)
        myreturn = "{}\n".format(myreturn)
      return myreturn
    def addCard(self, x, y, card):
      self.field[x][y] = card

class Action:
  def __init__(self):
    pass

class WheelSpace:
    def __init__(self, value):
      self.value = value
      self.resources = []
class Rondel:
    def __init__(self):
      self.currrent_turn = 0
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
    def nextTurn():
      self.current_turn += 1

class RondelProgression:
    def __init__(self, number_of_players):
      self.progression = {'1':{'long':[], 'short':[]},
                          '2':{'long':[], 'short':[]},
                          '3':{'long':[], 'short':[]},
                          '4':{'long':[], 'short':[]},}
      self.progression.append([])
forest = Card('Forest', 'Take Wood')
peat = Card('Peat Bog', 'Take Peat')

field_main = Playfield(5, 2)

field_main.addCard(card=forest, x=0, y=1)
field_main.addCard(card=forest, x=0, y=2)
field_main.addCard(card=forest, x=1, y=1)
field_main.addCard(card=peat, x=0, y=0)
field_main.addCard(card=peat, x=1, y=0)

print(field_main)
