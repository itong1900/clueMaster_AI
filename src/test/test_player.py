
## import first_module

#print("first_module's __name__: {}".format(first_module.__name__))
# print("second MOdule's name: {}".format(__name__))


import unittest
import sys
sys.path.append("../main/")
from Player import Player


class TestPlayer(unittest.TestCase):

    def test_must_have_updates(self):
        agent = Player("Jerry", 6)
        agent.update_suspect_must_have("Miss Peach")
        agent.update_suspect_must_have("Miss Scarlet")
        self.assertEqual(agent.suspect_must_have, {"Miss Scarlet", "Miss Peach"})

        agent.update_room_must_have("Poison")
        agent.update_room_must_have("Poison")
        self.assertEqual(agent.room_must_have, {"Poison"})

    def test_possibly_have_updates(self):
        agent = Player("Jerry", 6)
        agent.update_suspect_possibly_have("Miss Peach", 0.5)
        self.assertEqual(agent.suspect_possibly_have, {"Miss Peach": 0.5})
        agent.update_suspect_possibly_have("Miss Peach", 0.3)
        self.assertEqual(agent.suspect_possibly_have, {"Miss Peach":0.8})

if __name__ == '__main__':
    unittest.main()



