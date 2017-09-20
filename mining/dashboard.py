#! /usr/bin/env python3

"""
MODULE DOCS
"""


class Dashboard:

    def __init__(self, overlord):
        self.name = "DASHBOARD"
        self.overlord = overlord
        self.map_ids = list(self.overlord.graphs.keys())
        self.maps = {}
        
        for map_id in self.map_ids:
            self.maps[map_id] = '?'

    def __str__(self):
        border = '=' * 30
        output = []
        for key in self.maps.keys():
            output.append(border)
            output.append("\nMap ID: {}\n".format(key))
            output.append(border)
            output.append('\n')
            output.append(self.convert_to_string(key))
        output.append(border)
        return "".join([item for item in output if item])
        
    # list of keys should be list of keys from graph object
    def convert_to_string(self, map_id):
        """ Take a list of keys and convert graph obj data to string """
        
        list_of_keys = list([key for key in self.overlord.graphs[map_id].cells_dict.keys()])
        
        # Sort the graph keys based on x values then, based on y values
        sorted_graph_x = sorted(list_of_keys, key=lambda tup: (tup[0]))
        sorted_graph_y = sorted(list_of_keys, key=lambda tup: (tup[1]))
        
        try:
            # Get the size of the known map based on max & min, x & y values
            min_x = sorted_graph_x[0][0]
            max_x = sorted_graph_x[-1][0]
            min_y = sorted_graph_y[0][1]
            max_y = sorted_graph_y[-1][1]

            map_output = []
            # y value represent the rows value
            for y in range(max_y, min_y - 1 , -1):
                # x values represent the columns value
                for x in range(min_x, max_x + 1 ):
                    try:
                        map_output.append(self.overlord.graphs[map_id].cells_dict[(x,y)].symbol)
                    except KeyError:
                        map_output.append("?")
                map_output.append('\n')
            return ("".join(map_output))
        except IndexError:
            pass
