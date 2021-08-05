import unittest
import sys
sys.path.append("../main/")
from Advisor import Advisor

from unittest.mock import patch
from unittest import TestCase
# from unittest.mock import Mock
#advisor1 = Advisor(4)


class TestAdvisor(unittest.TestCase):
    
    
    @patch("builtins.input", side_effect = ["6", "Miss Peach,  Mr. Green","  Rope, Wrench", " Studio , Conservatory", " Mia ,7"," Michael ,7","Jane,7","Exit"])
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

    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White, Mrs Peacock, Colonel Mustard, Professor Plum, Miss Peach",
    "None", "None", "Mia, 7", "Michael, 6","Jane,7", "Exit"])
    def test_Game2_setup(self, mock_inputs):
        Advisor2 = Advisor(4)
        self.assertEqual(Advisor2.suspects, ["Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Colonel Mustard", "Professor Plum", "Miss Peach"])
        self.assertEqual(Advisor2.weapons, [])
        self.assertEqual(Advisor2.rooms, [])
        self.assertEqual(Advisor2.cardsIhave, 7)
        self.assertEqual(Advisor2.players["myself"].suspect_must_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", 
        "Colonel Mustard", "Professor Plum", "Miss Peach"})
        self.assertEqual(Advisor2.players["myself"].suspect_must_not_have, {"Sgt. Gray", "Monsieur Brunette", "Mme. Rose"})
        self.assertEqual(Advisor2.players["myself"].weapon_must_have, set())
        self.assertEqual(Advisor2.players["myself"].weapon_must_not_have, {"Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", 
        "Wrench", "Horseshoe", "Poison"})
        self.assertEqual(Advisor2.players["myself"].room_must_have, set())
        self.assertEqual(Advisor2.players["myself"].room_must_not_have, {"Carriage House", "Conservatory", "Kitchen", "Trophy Room", 
        "Dining Room", "Drawing Room", "Gazebo", "Courtyard", "Fountain", "Library", "Billiard Room", "Studio"})

        self.assertEqual(Advisor2.players["secret"].numberOfCards, 3)
        self.assertEqual(Advisor2.players["secret"].suspect_must_have, set())
        self.assertEqual(Advisor2.players["secret"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", 
        "Colonel Mustard", "Professor Plum", "Miss Peach"})
        self.assertEqual(Advisor2.players["secret"].weapon_must_have, set())
        self.assertEqual(Advisor2.players["secret"].weapon_must_not_have, set())
        self.assertEqual(Advisor2.players["secret"].room_must_have, set())
        self.assertEqual(Advisor2.players["secret"].room_must_not_have,set())

        self.assertEqual(Advisor2.players["secret"].suspect_possibly_have, {"Sgt. Gray":1/3, "Monsieur Brunette":1/3, "Mme. Rose":1/3})
        self.assertEqual(Advisor2.players["secret"].weapon_possibly_have, {"Candlestick":0.125, "Knife":0.125, "Lead Pipe":0.125, "Revolver":0.125, 
        "Rope":0.125, "Wrench":0.125, "Horseshoe":0.125, "Poison":0.125})
        self.assertEqual(Advisor2.players["secret"].room_possibly_have, {"Carriage House":1/12, "Conservatory":1/12, "Kitchen":1/12, "Trophy Room":1/12, 
        "Dining Room":1/12, "Drawing Room":1/12, "Gazebo":1/12, "Courtyard":1/12, "Fountain":1/12, "Library":1/12, "Billiard Room":1/12, "Studio":1/12})

        prob = 1/(30-7-3)
        self.assertEqual(Advisor2.players["Michael"].suspect_possibly_have, {"Sgt. Gray":prob*6, "Monsieur Brunette":prob*6, "Mme. Rose":prob*6})
        self.assertEqual(Advisor2.players["Michael"].weapon_possibly_have, {"Candlestick":prob*6, "Knife":prob*6, "Lead Pipe":prob*6, "Revolver":prob*6, 
        "Rope":prob*6, "Wrench":prob*6, "Horseshoe":prob*6, "Poison":prob*6})
        self.assertEqual(Advisor2.players["Michael"].room_possibly_have, {"Carriage House":prob*6, "Conservatory":prob*6, "Kitchen":prob*6, "Trophy Room":prob*6, 
        "Dining Room":prob*6, "Drawing Room":prob*6, "Gazebo":prob*6, "Courtyard":prob*6, "Fountain":prob*6, "Library":prob*6, "Billiard Room":prob*6, "Studio":prob*6})

        self.assertEqual(Advisor2.players["Jane"].suspect_possibly_have, {"Sgt. Gray":prob*7, "Monsieur Brunette":prob*7, "Mme. Rose":prob*7})

       
    # Game with 1 myself round
    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White", "Rope, Wrench", "Studio, Conservatory", "Mia, 7", "Michael, 6","Jane,7", 
    "Next turn", "myself", "Miss Peach, Revolver, Gazebo", "Michael, Jane, Mia", "Exit"])
    def test_Game3_setup(self, mock_inputs):
        Advisor3 = Advisor(4)
        self.assertEqual(Advisor3.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(Advisor3.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["secret"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["Mia"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["Jane"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})

        prob = 1/(30-7-3)
        self.assertEqual(Advisor3.players["myself"].suspect_must_have, {"Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["Jane"].suspect_possibly_have, {"Mrs Peacock": prob*7, "Colonel Mustard":prob*7, 
        "Professor Plum":prob*7, "Sgt. Gray":prob*7, "Monsieur Brunette":prob*7, "Mme. Rose":prob*7})
        self.assertEqual(Advisor3.players["Michael"].suspect_possibly_have, {"Mrs Peacock": prob*6, "Colonel Mustard":prob*6, 
        "Professor Plum":prob*6, "Sgt. Gray":prob*6, "Monsieur Brunette":prob*6, "Mme. Rose":prob*6})
        self.assertEqual(Advisor3.players["Mia"].suspect_possibly_have, {"Mrs Peacock": prob*7, "Colonel Mustard":prob*7, 
        "Professor Plum":prob*7, "Sgt. Gray":prob*7, "Monsieur Brunette":prob*7, "Mme. Rose":prob*7})
        
        self.assertEqual(Advisor3.players["Jane"].weapon_possibly_have, {"Candlestick":prob*7, "Knife":prob*7, "Lead Pipe":prob*7, 
        "Horseshoe":prob*7, "Poison":prob*7})
        # self.assertEqual(Advisor3.players["Michael"].weapon_possibly_have, {"Mrs Peacock": prob*6, "Colonel Mustard":prob*6, 
        # "Professor Plum":prob*6, "Sgt. Gray":prob*6, "Monsieur Brunette":prob*6, "Mme. Rose":prob*6})
        # self.assertEqual(Advisor3.players["Mia"].weapon_possibly_have, {"Mrs Peacock": prob*7, "Colonel Mustard":prob*7, 
        # "Professor Plum":prob*7, "Sgt. Gray":prob*7, "Monsieur Brunette":prob*7, "Mme. Rose":prob*7})


if __name__ == '__main__':
    unittest.main()