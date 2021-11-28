import unittest
import sys

sys.path.append("../main/")
from map import map

sys.path.append("../utils/")
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM

from unittest.mock import patch
from unittest import TestCase



class TestMap(unittest.TestCase):
    # check setup is ok
    def test_map(self):
        the_map = map()

        self.assertEqual(the_map.getShortestDistanceToOtherRooms("Trophy_Room"), {'Cloak_Room_Entry': 6, 'Kitchen': 8, 'Trophy_Room': 0, 'Dinning_Room': 12, 'Drawing_Room': 6, 
        'Gazebo': 12, 'Courtyard': 12, 'Fountain': 12, 'Library': 8, 'Billiard_Room': 11, 'Studio': 7, 'Conservatory': 6, 'Carriage_House': 2, 'Magnifier_1': 4, 'Magnifier_2': 11, 
        'Magnifier_3': 10, 'Magnifier_4': 13, 'Magnifier_5': 12, 'Magnifier_6': 13, 'Magnifier_7': 9, 'Magnifier_8': 9, 'Magnifier_9': 8})

        self.assertEqual(the_map.getShortestDistanceToOtherRooms('Carriage_House'), {'Cloak_Room_Entry': 8, 'Kitchen': 10, 'Trophy_Room': 2, 'Dinning_Room': 14, 'Drawing_Room': 8, 
        'Gazebo': 14, 'Courtyard': 14, 'Fountain': 14, 'Library': 10, 'Billiard_Room': 13, 'Studio': 9, 'Conservatory': 8, 'Carriage_House': 0, 'Magnifier_1': 6, 'Magnifier_2': 13, 
        'Magnifier_3': 12, 'Magnifier_4': 15, 'Magnifier_5': 14, 'Magnifier_6': 15, 'Magnifier_7': 11, 'Magnifier_8': 11, 'Magnifier_9': 10})

 
if __name__ == '__main__':
    unittest.main()
