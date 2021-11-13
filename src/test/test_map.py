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
        print(the_map.distance_map["Cloak_Room_Entry"].distance_others)
        print(the_map.getReachableRoom(7, "Cloak_Room_Entry"))
 
if __name__ == '__main__':
    unittest.main()
