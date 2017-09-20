#! /usr/bin/env python3

class Cell:
    """ A cell holds its neighbors and symbols in them """

    def __init__(self, node):
        self.id = node
        self.symbol = "?"
        self.adjacent = {}

    def __str__(self):
        return str(self.id), str([x.id for x in self.adjacent])
    
    def __eq__(self, other):
        # print("COMPARING KEYS")
        # print(self.id, other.id)
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
        # print(type(neighbor), type(data))
        # print("beginning", self.id, self.symbol, "Adding Neighbor ", neighbor)
        # print("Attempting to set cell symbel", neighbor.id, data[1])
        self.adjacent[neighbor] = data

    def get_connection(self):
        return self.adjacent.keys()

    def get_direction(self, neighbor):
        return self.adjacent[neighbor][0]

    def get_symbol(self, neighbor):
        return self.adjacent[neighbor][1]

    def __str__(self):
        return str(self.id) + self.symbol +' Adjacent: ' + str([x.id for x in self.adjacent])


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
        # print("adding node", type(node))
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

        # print("Looking to find a place to insert the symbol into cell.symbol", type(dst), dst, type(data), data)
        
        if src not in self.cells_dict:
            self.add_cell(src)
        if dst not in self.cells_dict:
            # print(dst, "Symbol = [ ", data[1], ']')
            self.add_cell(dst)
        # print(dst, data[1])
        self.cells_dict[dst].symbol = data[1]

        # print("adding src -> dest ")
        self.cells_dict[src].add_neighbor(self.cells_dict[dst], data)
        # print("adding dest -> src ")
        self.cells_dict[dst].add_neighbor(self.cells_dict[src], data)
    
    def get_cells(self):
        return self.cells_dict.keys()
