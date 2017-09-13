#! /usr/bin/env python3

import unittest
from zerg import *

class TestMining(unittest.TestCase):
    
    def test_make_overlord(self):
        new = Overlord(total_ticks=100, refined_minerals=100)
        self.assertTrue(hasattr(new, 'health'), True)
        self.assertTrue(new.ticks, 100)
        self.assertTrue(new.refined_minerals, 100)

    def test_make_base_drone(self):
        new = BaseDrone()
        self.assertTrue(hasattr(new, 'health'), True)
        self.assertEqual(new.get_init_cost(), 9)

    def test_make_scout_drone(self):
        new = ScoutDrone()
        self.assertTrue(hasattr(new, 'health'), True)
        self.assertEqual(new.get_init_cost(), 9)

    def test_make_hauler_drone(self):
        new = HaulerDrone()
        self.assertTrue(hasattr(new, 'health'), True)
        self.assertEqual(new.get_init_cost(), 9)

    def test_overlord_make_drones(self):
        new = Overlord()
        drone = BaseDrone()
        new.zerg[id(drone)] = drone
        self.assertTrue(len(new.zerg), 1)

    def test_overlord_add_map(self):
        new = Overlord()
        new.add_map(1, 1.15)
        self.assertTrue(len(new.maps), 1)
        self.assertTrue(new.maps[1], 1.15)
        new.add_map(2, 3.78)

if __name__ == "__main__":
    unittest.main()
