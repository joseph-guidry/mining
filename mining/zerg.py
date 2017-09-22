#! /usr/bin/env python3

"""
MODULE DOCUMENTATION
"""

import abc
from random import randint, choice
from mining.graph import *
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

    def __init__(self, ticks=1, refined_minerals=54):
        """ Constuct a Overlord with default values if not provided """
        self.health = 5
        self.ticks = ticks
        self.refined_minerals = refined_minerals
        self.zerg = {}
        self.maps = {}
        self.graphs = {}
        self.available_drones = []
        self.deployed_drones = {}

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

    def dashboard(self):
        return Dashboard(self)

    def action(self, map_context=None):
        """ Allows overlord to deploy, retrieve or None """
        """ This is based on drone ID """
        self.ticks -= 1
        print("Available", self.available_drones)
        print("Deployed ", self.deployed_drones)
        map_id = choice(list(self.graphs.keys()))
        print("Map_id ", map_id)

        # Check if drone has set its pickup flag for return.
        for drone in list(self.zerg.keys()):
            if self.zerg[drone].pick_up is True:
                self.reinitialize_drone(self.zerg[drone])
                self.available_drones.append(drone)
                self.deployed_drones.pop(drone, None)
                print("After returning drone", self.available_drones)
                return 'RETURN {}'.format(drone)
        
        # Get a list of the map_ids and send drone to a specific map
        # If there are more drones to deploy then do that.
        print("Available drones ", len(self.available_drones), self.available_drones)
        drone_to_map = list([drone for drone in self.deployed_drones.keys() 
                             if self.deployed_drones[drone] == map_id])
        for drone in drone_to_map:
            if self.zerg[drone].position == (0,0):
                print("Drone", drone, self.zerg[drone].position )
                return "NONE" 

        if len(self.available_drones) > 0:
            # print("DEPLOY")
            drone = self.available_drones.pop(0)
            # print("DRONE!!! ", drone)
            # print("Available ", self.available_drones)
            self.deployed_drones[drone] = map_id
            # print("Deployed ",self.deployed_drones)
            self.zerg[drone].map_id = map_id
            # print("Map_ID ", map_id)
            self.zerg[drone].graph = self.graphs[map_id]
            self.zerg[drone].ticks_start = self.ticks
            return 'DEPLOY {} {}'.format(drone, map_id)
        else:
            return "NONE"


    def reinitialize_drone(self, drone):
        """ Reset the values of a returned drone """
        drone.storage = drone.capacity 
        drone.pick_up = False
        drone.return_flag = False
        drone.previous_positions = []
        drone.list_xy = []
        drone.movements = 0


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
        self.movements = 0
        self.storage = self.capacity
        self.return_flag = False
        self.pick_up = False
        self.position = (0, 0)
        self.graph = None
        self.previous_direction = ""
        self.previous_positions = []
        self.list_xy = []

    @classmethod
    def get_init_cost(cls):
        """ Return the cost value for a drone object """
        return cls.init_value
    
    def steps(self):
        """ return the total number of steps taken by drone """
        return self.movements

    def action(self, context):
        
        """ Inherited method for all Drone subclasses """
        print("Starting turn: " + str(self.position) )
        print("Path taken", self.previous_positions)
        # This ensures the drone moved on the grid 
        # and will not add position to path
        try:
            
            moved = True
            self.list_xy.append( (context.x, context.y) )
            if self.list_xy[-1] == self.list_xy[-2]:
                # print("Didnt MOve this Turn")
                moved = False
                self.last_position = self.previous_positions[-1]
        except IndexError:
            pass

        # print("CHECKING IS POSTION CHANGED")
        # print(self.position, self.list_xy[-1])
        if self.return_flag is False and moved is True:
            self.previous_positions.append(self.position)

        # print("Start", self.ticks_start, "REmaining", self.overlord.ticks)

        x, y = self.position
        directions = [(x, y + 1), (x, y - 1), (x - 1, y), (x + 1, y)]
        contents = [ ["NORTH", context.north], ["SOUTH", context.south], 
                     ["WEST", context.west], ["EAST", context.east] ]
        # Variable to hold current data set for the current drone
        input_scheme = list(zip(directions, contents))
        
        # UPdate the graph data with surrounding information
        for i in range(4):
            dst, data = input_scheme[i]
            self.graph.add_edge(self.position, dst, data)
       
        # Indicate that a drone is ready for pickup.
        if (x, y) == (0,0) and self.movements > 0:
            print("On landing zone and have minerals")
            self.pick_up = True
            return "CENTER"

        """
        This is the drones decision making process after capacity is 
        full or time is running out
        """

        if self.movements + 1 >= self.overlord.ticks or self.storage <= 0:
            print("\tLETS to move backwards")
            self.return_flag = True
            return self.move_to_previous(self.position, input_scheme)

        """
        Keep attempt to find path with undiscovered cells, 
        after "CENTER" has been returned.
        """

        print("Is return flag set ? ", self.return_flag)
        if self.return_flag == True:
            print("WERE STUCK LETS BACK TRACK a bit")
            print("Previous Locations", self.previous_positions)
            adj_neighbors = [item for item in self.graph.cells_dict[self.position].adjacent.keys()]
            print(adj_neighbors)
            for neighbor in adj_neighbors:
                print(neighbor.id)
                print(neighbor.symbol)
        
                # Number of neighbors a coordinate has
                # print(len(self.graph.cells_dict[neighbor.id].adjacent))
        
                # A list of neighbors with their coordinates
                # neighbors = list([position.id for position in self.graph.cells_dict[neighbor.id].adjacent.keys()])
                # print("list of neighbors", neighbors)
                print("last position", self.last_position)
                if neighbor.id not in self.previous_positions:
                    if neighbor.id != self.last_position and neighbor.symbol in '* ':
                        print("Moving somewhere", neighbor.id)
                        # Need to return direction to this ID!!!
                        # print(self.graph.cells_dict[self.position].adjacent)
                        get_direction = [item for item in self.graph.cells_dict[self.position].adjacent.keys()]
                        print("number of adj", len(get_direction))
                        print("Direction", input_scheme)
                        for next in input_scheme:
                            print("checking the input scheme", next)
                            if next[0] == neighbor.id:
                                self.return_flag = False
                                print( " LETS GO THIS WAY", next[1][0])
                                self.position = neighbor.id
                                # self.previous_positions.pop(-1)
                                return next[1][0]
                            
            print("LETS MOVE BACK ONE")
            return self.move_to_previous(self.position, input_scheme)

        if self.move_north(self.position) not in self.previous_positions and context.north in '* ':
            print("NORTH")
            self.previous_direction = "NORTH"
            if context.north in '*':
                #self.previous_positions.pop(-1)
                self.storage -= 1
                return 'NORTH'
            else:
                self.position = self.move_north(self.position)
                self.movements += 1
                return 'NORTH'
        elif self.move_east(self.position) not in self.previous_positions and context.east in '* ':
            print("EAST")
            self.previous_direction = "EAST"
            if context.east in '*':
                self.storage -= 1
                return 'EAST'
            else:
                self.position = self.move_east(self.position)
                self.movements += 1
                return 'EAST'
        elif self.move_south(self.position) not in self.previous_positions and context.south in '* ':
            print("SOUTH")
            self.previous_direction = "SOUTH"
            if context.south in '*':
                self.storage -= 1
                return 'SOUTH'
            else:
                self.position = self.move_south(self.position)
                self.movements += 1
                return 'SOUTH'
        elif self.move_west(self.position) not in self.previous_positions and context.west in '* ':
            print("WEST")
            self.previous_direction = "WEST"
            if context.west in '*':
                self.storage -= 1
                return 'WEST'
            else:
                self.position = self.move_west(self.position)
                self.movements += 1
                return 'WEST'
        else:
            print("CENTER")
            self.previous_direction = "CENTER"
            self.return_flag = True
            return 'CENTER'

    def move_to_previous(self, position, input_scheme):
        try:
            self.last_position = self.previous_positions[-1]
            for dir_context in input_scheme:
                print("dir_context", dir_context)
                if dir_context[0] == self.previous_positions[-2]:
                    print("DIRECTION ", dir_context[1][0])
                    self.position = self.previous_positions[-2]
                    self.previous_positions.pop(-1)
                    return dir_context[1][0]
        except IndexError:
            pass


    def move_north(self, position):
        """ Increment position north """
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
    

class ScoutDrone(Drone):
    """ Extend Drone class to specialized scout Drone """
    """ Health = 20, Capacity = 5, Move = 2 """

    init_value = 9

    def __init__(self, health=2, capacity=1, moves=6, overlord=None):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves, overlord)


class HaulerDrone(Drone):
    """ Extend Drone class to specialized hauler Drone """
    """ Health = 20, Capacity = 20, Move = 1 """

    init_value = 9

    def __init__(self, health=1, capacity=5, moves=3, overlord=None):
        """ Constructor for Base Drone, pass number of refined minerals"""
        super().__init__(health, capacity, moves, overlord)
