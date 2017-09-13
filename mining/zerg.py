#! /usr/bin/env python3

"""
MODULE DOCUMENTATION
"""

import abc
from random import randint, choice
    
class Zerg(metaclass=abc.ABCMeta):
    """ Abstract zerg for API """

    @property
    def health(self):
        """ Requires the health attribute for all zergs"""
        return self._health

    @health.setter
    def health(self, health):
        self._health = health

    @abc.abstractmethod 
    def action(self, map_context):
        """ Method required by all zerg types """
        pass

class Overlord(Zerg):
    """ Overlord Zerg Class """

    def __init__(self, total_ticks=1, refined_minerals=54):
        """ Constuct a Overlord with default values if not provided """
        self.health = 5
        self.ticks = total_ticks
        self.refined_minerals = refined_minerals
        self.zerg = {}
        self.maps = {}

        for _ in range(1):
            z = BaseDrone()
            self.zerg[id(z)] = z          

    def add_map(self, map_id, summary):
        """ Allows Overlord to know about multiple maps? """
        self.maps[map_id] = summary

    def action(self, map_context=None):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
        act = randint(0, 3)
        if act == 0:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        else:
            return 'DEPLOY {} {}'.format(choice(list(self.zerg.keys())),
                    choice(list(self.maps.keys())))


class Drone(Zerg):
    """ This is base drone class """

    def __init__(self, health, capacity, moves):
        """ Parent Drone Constructor """
        """ Constructor for Base Drone, pass number of refined minerals"""
        self.health = health * 10
        self.capacity = capacity * 5
        self.moves = int(moves / 3)
        self.steps = 0

    @classmethod
    def get_init_cost(cls):
        """ Return the cost value for a drone object """
        return cls.init_value

    def steps(self):
        """ return the total number of steps taken by drone """
        return self.steps

    def action(self, context):
        """ Inherited method for all Drone subclasses """
        new = randint(0, 3)
        if new == 0 and context.north in '* ':
            self.steps += 1
            return 'NORTH'
        elif new == 1 and context.south in '* ':
            self.steps += 1
            return 'SOUTH'
        elif new == 2 and context.east in '* ':
            self.steps += 1
            return 'EAST'
        elif new == 3 and context.west in '* ':
            self.steps += 1
            return 'WEST'
        else:
            return 'CENTER'


class BaseDrone(Drone):
    """ Extend the drone class to default drones """
    """ Health = 40, Capacity = 10, Move = 1 """
    
    init_value = 9
    
    def __init__(self, health=4, capacity=2, moves=3):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves)
    
    # def action(self, map_context):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
        # pass


class ScoutDrone(Drone):
    """ Extend Drone class to specialized scout Drone """
    """ Health = 20, Capacity = 5, Move = 2 """

    init_value = 9

    def __init__(self, health=2, capacity=1, moves=6):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves)

    # def action(self, map_context):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
       # pass
    

class HaulerDrone(Drone):
    """ Extend Drone class to specialized hauler Drone """
    """ Health = 20, Capacity = 20, Move = 1 """

    init_value = 9

    def __init__(self, health=1, capacity=5, moves=3):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves)

    # def action(self, map_context):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
       # pass
