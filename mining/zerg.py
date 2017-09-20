#! /usr/bin/env python3

"""
MODULE DOCUMENTATION
"""

import abc
from random import randint, choice
from mining.grid import *
from mining.dashboard import *
    
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
        self.graphs = {}
        self.available_drones = []
        self.deployed_drones = []

        for _ in range(1):
            z = BaseDrone(overlord=self)
            self.refined_minerals -= z.get_init_cost()
            self.zerg[id(z)] = z

        for drone_id in self.zerg.keys():
            self.available_drones.append(drone_id)

    def add_map(self, map_id, summary):
        """ Allows Overlord to know about multiple maps? """
        self.maps[map_id] = summary
        self.graphs[map_id] = Graph()

    def get_dashboard(self):
        return Dashboard(self)

    def action(self, map_context=None):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
        self.ticks -= 1
        print(self.available_drones)
        map_id = choice(list(self.graphs.keys()))
        print("Map_id ", map_id)

        # Get the list of keys from a graph based on map_id

        # Check if drone has set its pickup flag for return.
        for drone in list(self.zerg.keys()):
            
            if self.zerg[drone].pick_up is True or self.zerg[drone].capacity < 5:
                self.zerg[drone].pick_up = False
                self.zerg[drone].return_flag = False
                self.zerg[drone].steps = 0
                self.available_drones.append(drone)
                print("After returning drone", self.available_drones)
                return 'RETURN {}'.format(drone)
        
        # Get a list of the map_ids and send drone to a specific map
        # If there are more drones to deploy then do that.
        print("Available drones ", len(self.available_drones), self.available_drones)
        if len(self.available_drones) > 0:
            print("DEPLOY")
            drone = self.available_drones.pop()
            print("DRONE!!! ", drone)
            print("Available ", self.available_drones)
            self.deployed_drones.append(drone)
            print("Deployed ",self.deployed_drones)
            self.zerg[drone].map_id = map_id
            print("Map_ID ", map_id)
            self.zerg[drone].graph = self.graphs[map_id]
            self.zerg[drone].ticks_start = self.ticks
            return 'DEPLOY {} {}'.format(drone, map_id)
        else:
            print("NONE")
            return "NONE"

class Drone(Zerg):
    """ This is base drone class """

    def __init__(self, health, capacity, moves, overlord):
        """ Parent Drone Constructor """
        """ Constructor for Base Drone, pass number of refined minerals"""
        self.overlord = overlord
        self.map_id = -1
        self.health = health * 10
        self.capacity = capacity * 5
        self.moves = int(moves / 3)
        self.ticks_start = 0
        self.steps = 0
        self.return_flag = False
        self.pick_up = False
        self.position = (0, 0)
        self.graph = None
        self.previous_direction = ""
        self.previous_positions = []
        

    @classmethod
    def get_init_cost(cls):
        """ Return the cost value for a drone object """
        return cls.init_value

    def steps(self):
        """ return the total number of steps taken by drone """
        return self.steps

    def action(self, context):
        """ Inherited method for all Drone subclasses """
        print("Starting turn: " + str(self.position) )

        x, y = self.position
        directions = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
        contents = [ ["NORTH", context.north], ["SOUTH", context.south], 
                     ["WEST", context.west], ["EAST", context.east] ]
        input_scheme = list(zip(directions, contents))
        
        print(input_scheme)
        
        for i in range(4):
            dst, data = input_scheme[i]
            self.graph.add_edge(self.position, dst, data)
       
        if (x, y) == (0,0) and self.steps > 0:
            print("On landing zone and have minerals")
            self.pick_up = True
            return "CENTER"

        print(self.previous_positions)
        # Get all position coordinates -> if not in path go that way.
        # Else go back to last position?
        print(self.steps, self.overlord.ticks)
        if self.steps + 1 >= self.overlord.ticks or self.capacity <= 0:
            self.return_flag = True
            print(self.previous_positions)
            print("Last Position ", self.previous_positions[-1])
            print("Available directions " ,input_scheme)
            for dir_context in input_scheme:
                if dir_context[0] == self.previous_positions[-1]:
                    print("DIRECTION ", dir_context[1][0])
                    self.position = self.previous_positions[-1]
                    self.previous_positions.pop(-1)
                    return dir_context[1][0]

        # Keep attempt to find path with undiscovered cells -> check in graph?
        if self.previous_direction == "CENTER":
            print("WERE STUCK LETS BACK TRACK a bit")

        # Could be removed?
        print(self.position)
        if self.return_flag is False:
            print("Adding current position")
            self.previous_positions.append(self.position)

        
        if self.move_north(self.position) not in self.previous_positions and context.north in '* ':
            print("NORTH")
            self.previous_direction = "NORTH"
            if context.north in '*':
                self.previous_positions.pop(-1)
                self.capacity -= 1
                return 'NORTH'
            else:
                self.position = self.move_north(self.position)
                self.steps += 1
                return 'NORTH'
        elif self.move_east(self.position) not in self.previous_positions and context.east in '* ':
            print("EAST")
            self.previous_direction = "EAST"
            if context.east in '*':
                self.previous_positions.pop(-1)
                self.capacity -= 1
                return 'EAST'
            else:
                self.position = self.move_east(self.position)
                self.steps += 1
                return 'EAST'
        elif self.move_south(self.position) not in self.previous_positions and context.south in '* ':
            print("SOUTH")
            self.previous_direction = "SOUTH"
            if context.south in '*':
                self.previous_positions.pop(-1)
                self.capacity -= 1
                return 'SOUTH'
            else:
                self.position = self.move_south(self.position)
                self.steps += 1
                return 'SOUTH'
        elif self.move_west(self.position) not in self.previous_positions and context.west in '* ':
            print("WEST")
            self.previous_direction = "WEST"
            if context.west in '*':
                self.previous_positions.pop(-1)
                self.capacity -= 1
                return 'WEST'
            else:
                self.position = self.move_west(self.position)
                self.steps += 1
                return 'WEST'
        else:
            self.previous_direction = "CENTER"
            return 'CENTER'


    def move_north(self, position):
        """ Increment position north """
        # print("Position: " + str(position))
        x, y = position
        return (x, y + 1)

    def move_south(self, position):
        """ Increment position south """
        x, y = position
        return (x, y - 1)

    def move_east(self, position):
        """ Increment position east """
        x, y = position
        return (x + 1, y)

    def move_west(self, position):
        """ Increment position east """
        x, y = position
        return (x - 1, y)

        

class BaseDrone(Drone):
    """ Extend the drone class to default drones """
    """ Health = 40, Capacity = 10, Move = 1 """
    
    init_value = 9
    
    def __init__(self, health=4, capacity=2, moves=3, overlord=None):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves, overlord)
    
    # def action(self, map_context):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
        # pass


class ScoutDrone(Drone):
    """ Extend Drone class to specialized scout Drone """
    """ Health = 20, Capacity = 5, Move = 2 """

    init_value = 9

    def __init__(self, health=2, capacity=1, moves=6, overlord=None):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves, overlord)

    # def action(self, map_context):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
       # pass
    

class HaulerDrone(Drone):
    """ Extend Drone class to specialized hauler Drone """
    """ Health = 20, Capacity = 20, Move = 1 """

    init_value = 9

    def __init__(self, health=1, capacity=5, moves=3, overlord=None):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves, overlord)

    # def action(self, map_context):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
       # pass
