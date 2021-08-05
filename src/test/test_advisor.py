import unittest
import sys
sys.path.append("../main/")
from Advisor import Advisor

from unittest.mock import patch
from unittest import TestCase
# from unittest.mock import Mock
# advisor1 = Advisor(4)


class TestAdvisor(unittest.TestCase):
    
    
    @patch("builtins.input", side_effect = ["6", "Miss Peach   ,  Mr. Green","  Rope, Wrench", " Studio , Conservatory", " Mia ,7"," Michael ,7","Jane,7","Exit"])
    def test_Game1_setup(self, mock_inputs):
        Advisor1 = Advisor(4)
        self.assertEqual(Advisor1.suspects, ["Miss Peach", "Mr. Green"])
        self.assertEqual(Advisor1.weapons, ["Rope", "Wrench"])
        self.assertEqual(Advisor1.rooms, ["Studio", "Conservatory"])
        self.assertEqual(Advisor1.cardsIhave, 6)
        self.assertEqual(Advisor1.players["secret"].name, "secret")
        self.assertEqual(Advisor1.players["secret"].numberOfCards, 3)
        self.assertEqual(Advisor1.players["secret"].suspect_must_have, set())
        self.assertEqual(Advisor1.players["secret"].suspect_must_not_have, {"Miss Peach", "Mr. Green"})
        self.assertEqual(Advisor1.players["secret"].weapon_must_have, set())
        self.assertEqual(Advisor1.players["secret"].weapon_must_not_have, {"Rope", "Wrench"})
        self.assertEqual(Advisor1.players["secret"].room_must_have, set())
        self.assertEqual(Advisor1.players["secret"].room_must_not_have, {"Studio", "Conservatory"})
        self.assertEqual(Advisor1.players["secret"].suspect_possibly_have, {"Miss Scarlet":0.125, "Mrs White":0.125, "Mrs Peacock":0.125, "Colonel Mustard":0.125, 
        "Professor Plum":0.125, "Sgt. Gray":0.125, "Monsieur Brunette":0.125, "Mme. Rose":0.125})
        self.assertEqual(Advisor1.players["secret"].weapon_possibly_have, {"Candlestick": 1/6, "Knife":1/6, "Lead Pipe":1/6, 
        "Revolver":1/6, "Horseshoe":1/6, "Poison":1/6})
        self.assertEqual(Advisor1.players["secret"].room_possibly_have, {"Carriage House":0.1, "Kitchen":0.1, "Trophy Room":0.1, "Dining Room":0.1, 
        "Drawing Room":0.1, "Gazebo":0.1, "Courtyard":0.1, "Fountain":0.1, "Library":0.1, "Billiard Room":0.1})

        prob = 1/(30-6-3)
        self.assertEqual(Advisor1.players["Mia"].suspect_possibly_have, {"Miss Scarlet": prob*7, "Mrs White":prob*7, "Mrs Peacock":prob*7, "Colonel Mustard":prob*7, 
        "Professor Plum":prob*7, "Sgt. Gray":prob*7, "Monsieur Brunette":prob*7, "Mme. Rose":prob*7})
        self.assertEqual(Advisor1.players["Mia"].weapon_possibly_have, {"Candlestick": prob*7, "Knife":prob*7, "Lead Pipe":prob*7, 
        "Revolver":prob*7, "Horseshoe":prob*7, "Poison":prob*7})
        self.assertEqual(Advisor1.players["Mia"].room_possibly_have, {"Carriage House":prob*7, "Kitchen":prob*7, "Trophy Room":prob*7, "Dining Room":prob*7, 
        "Drawing Room":prob*7, "Gazebo":prob*7, "Courtyard":prob*7, "Fountain":prob*7, "Library":prob*7, "Billiard Room":prob*7})



if __name__ == '__main__':
    unittest.main()