#!/usr/local/bin/python

from random import randint, choice

class Drone:
    def __init__(self):
        self.health = 25
        self.moves = randint(1,6)

    def action(self, context):
        new = randint(0, 3)
        if new == 0 and context.north in '* ':
            return 'NORTH'
        elif new == 1 and context.south in '* ':
            return 'SOUTH'
        elif new == 2 and context.east in '* ':
            return 'EAST'
        elif new == 3 and context.west in '* ':
            return 'WEST'
        else:
            return 'CENTER'

class Overlord:
    def __init__(self, total_ticks):
        self.maps = {}
        self.zerg = {}

        for _ in range(6):
            z = Drone()
            self.zerg[id(z)] = z

    def add_map(self, map_id, summary):
        self.maps[map_id] = summary

    def action(self):
        act = randint(0, 3)
        if act == 0:
            return 'RETURN {}'.format(choice(list(self.zerg.keys())))
        else:
            return 'DEPLOY {} {}'.format(choice(list(self.zerg.keys())),
                    choice(list(self.maps.keys())))


"""
#! /usr/bin/env python3

"""
MODULE DOCUMENTATION
"""

import abc

    
class Zerg(metaclass=abc.ABCMeta):
    """ Abstract zerg for API """

    @abstractproperty
    def health(self, value):
        """ Requires the health attribute for all zergs"""
        return 'This is not good'

    @abc.abstractmethod 
    def action(self, map_context):
        """ Method required by all zerg types """

class Overload(Zerg):
    """ Overlord Zerg Class """

    def __init__(self, total_ticks=1, refined_minerals=54)
        """ Constuct a Overlord with default values if not provided """
        pass

    def add_map(self, map_id, summary):
        """ Allows Overlord to knwo about multiple maps? """
        pass

    def action(self, map_context):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
        pass


class Drone(Zerg):
    """ This is base drone class """
    
    def __init__(self):
        """ Create a base drone with default values """
        super().__init__()
        
"""
