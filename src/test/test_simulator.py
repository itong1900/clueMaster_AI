import unittest
import sys

#from main.Simulator import Simulator
sys.path.append("../main/")
from Simulator import Simulator

sys.path.append("../utils/")
from config_CONST import LIST_SUSPECT, LIST_WEAPON, LIST_ROOM

from unittest.mock import patch
from unittest import TestCase
import math


class TestSimulator(unittest.TestCase):

    # check setup is ok
    def test_Game2_setup(self):
        Simulator1 = Simulator(5)

        SET_SUSPECT = set(LIST_SUSPECT)
        SET_WEAPON = set(LIST_WEAPON)
        SET_ROOM = set(LIST_ROOM)

        simulator_suspect = set()
        simulator_suspect = simulator_suspect.union(set(Simulator1.agent_hashmap["Player_0"].suspects))
        simulator_suspect = simulator_suspect.union(set(Simulator1.agent_hashmap["Player_1"].suspects))
        simulator_suspect = simulator_suspect.union(set(Simulator1.agent_hashmap["Player_2"].suspects))
        simulator_suspect = simulator_suspect.union(set(Simulator1.agent_hashmap["Player_3"].suspects))
        simulator_suspect = simulator_suspect.union(set(Simulator1.agent_hashmap["Player_4"].suspects))
        simulator_suspect.add(Simulator1.secrets[0])

        self.assertEqual(simulator_suspect, SET_SUSPECT)

        simulator_weapon = set()
        simulator_weapon = simulator_weapon.union(set(Simulator1.agent_hashmap["Player_0"].weapons))
        simulator_weapon = simulator_weapon.union(set(Simulator1.agent_hashmap["Player_1"].weapons))
        simulator_weapon = simulator_weapon.union(set(Simulator1.agent_hashmap["Player_2"].weapons))
        simulator_weapon = simulator_weapon.union(set(Simulator1.agent_hashmap["Player_3"].weapons))
        simulator_weapon = simulator_weapon.union(set(Simulator1.agent_hashmap["Player_4"].weapons))
        simulator_weapon.add(Simulator1.secrets[1])

        self.assertEqual(simulator_weapon, SET_WEAPON)

        simulator_room = set()
        simulator_room = simulator_room.union(set(Simulator1.agent_hashmap["Player_0"].rooms))
        simulator_room = simulator_room.union(set(Simulator1.agent_hashmap["Player_1"].rooms))
        simulator_room = simulator_room.union(set(Simulator1.agent_hashmap["Player_2"].rooms))
        simulator_room = simulator_room.union(set(Simulator1.agent_hashmap["Player_3"].rooms))
        simulator_room = simulator_room.union(set(Simulator1.agent_hashmap["Player_4"].rooms))
        simulator_room.add(Simulator1.secrets[2])

        self.assertEqual(simulator_room, SET_ROOM)
        
        self.assertEqual(Simulator1.agent_hashmap["Player_0"].numcardsIhave + Simulator1.agent_hashmap["Player_1"].numcardsIhave
        + Simulator1.agent_hashmap["Player_2"].numcardsIhave + Simulator1.agent_hashmap["Player_3"].numcardsIhave 
        + Simulator1.agent_hashmap["Player_4"].numcardsIhave, 27)

        print(Simulator1.agent_hashmap["Player_0"].myhint)
        print(Simulator1.agent_hashmap["Player_0"].suspects)
        print(Simulator1.agent_hashmap["Player_0"].weapons)
        print(Simulator1.agent_hashmap["Player_0"].rooms)
        print(Simulator1.agent_hashmap["Player_0"].players["Player_1"].display_player_summary("Player_1"))


    def test_Game2_setup(self):
        Simulator2 = Simulator(4, 8)

        #Simulator2.agent_hashmap["Player_2"].players["Player_1"].display_suspect_must_have()
        print(Simulator2.solutions)

if __name__ == '__main__':
    unittest.main()