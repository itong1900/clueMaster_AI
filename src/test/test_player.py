import unittest
from clueMaster_AI.src.main.Player import Player

class TestPlayer(unittest.TestCase):

    def test_update_suspect_must_have(self):
        agent = Player.Player()
        agent.update_suspect_must_have("Miss Peach")
        self.assertEqual(agent.suspect_must_have, {"Miss Peach"})

if __name == '__main__':
    unittest.main()