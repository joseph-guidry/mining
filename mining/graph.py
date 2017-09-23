#! /usr/bin/env python3
"""
MODULE DOCUMENTATION
"""


class Cell:
    """ A cell holds its neighbors and symbols in them """

    def __init__(self, node):
        self.id = node
        self.symbol = "?"
        self.adjacent = {}
    
    def __str__(self):
        return str(self.id) + self.symbol +' Adjacent: ' + str([x.id for x in self.adjacent])

    def __eq__(self, other):
        x1, y1 = self.id
        x2, y2 = other.id
        return x1 == x2 and y1 == y2

    def _lt__(self, other):
        x1, y1 = self.id
        x2, y2 = other.id
        if x1 < x2:
            return True
        elif x1 == x2 and y1 < y2:
            return True
        return False

    def __gt__(self, other):
        x1, y1 = self.id
        x2, y2 = other.id
        if x1 > x2:
            return True
        elif x1 == x2 and y1 < y2:
            return True
        return False

    def __hash__(self):
        return super().__hash__()

    def add_neighbor(self, neighbor, data):
        """ Data = ["DIRECTION", "SYMBOL"] """
        self.adjacent[neighbor] = data

    def get_connection(self):
        return self.adjacent.keys()

    def get_direction(self, neighbor):
        return self.adjacent[neighbor][0]

    def get_symbol(self, neighbor):
        return self.adjacent[neighbor][1]


class Graph:
    """ Build a Graph """

    def __init__(self):
        """ Contains the nodes/tiles on the map """
        self.num_cell = 0
        self.num_zergs = 0
        self.cells_dict = {}

    def __str__(self):
        """ print the graph to see what is inside """
        output = []
        for key in self.cells_dict.keys():
            output.append(str(self.cells_dict[key]) )
            output.append('\n')
        return "".join(output)

    def __iter__(self):
        return iter(self.cells_dict.values())

    def add_cell(self, node):
        self.num_cell = self.num_cell + 1
        new_node = Cell(node)
        self.cells_dict[node] = new_node
        return new_node

    def get_cell(self, n):
        if n in self.cells_dict:
            return self.cells_dict[n]
        else:
            return None

    def add_edge(self, src, dst, data=None):
        """ Update the graph with the values at each adjacent cell """

        if src not in self.cells_dict:
            self.add_cell(src)
        if dst not in self.cells_dict:
            self.add_cell(dst)
        self.cells_dict[dst].symbol = data[1]

        self.cells_dict[src].add_neighbor(self.cells_dict[dst], data)
        self.cells_dict[dst].add_neighbor(self.cells_dict[src], data)
    
    def get_cells(self):
        """ Return the cells that are in the graph """
        return self.cells_dict.keys()
