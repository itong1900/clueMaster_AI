
## import first_module

#print("first_module's __name__: {}".format(first_module.__name__))
# print("second MOdule's name: {}".format(__name__))


import unittest
import sys
sys.path.append("../main/")
from Player import Player


class TestPlayer(unittest.TestCase):

    def test_update_suspect_must_have(self):
        agent = Player("Jerry", 6)
        agent.update_suspect_must_have("Miss Peach")
        self.assertEqual(agent.suspect_must_have, {"Miss Peach"})

if __name__ == '__main__':
    unittest.main()



