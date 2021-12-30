import unittest
import sys
sys.path.append("../main/")
from backend_test_ingest import backend_test_ingest

from unittest.mock import patch
from unittest import TestCase
import math


# from unittest.mock import Mock
#TesetObject.algo_this_advisor = Advisor(4)


class TestAdvisor(unittest.TestCase):
    
    # Advisor 3   
    # Game with 1 myself round
    @patch("builtins.input", side_effect = ["Advisor_Algo_I", "7", "Miss Scarlet, Mr. Green, Mrs White", "Rope, Wrench", "Studio, Conservatory", "Mia, 7", "Michael, 6","Jane,7", 
    "Next turn", "myself", "Miss Peach, Revolver, Gazebo", "Michael, Jane, Mia", 
    "Query", "Player_Summary", "Jane", "Exit"])
    def test_Game3_setup(self, mock_inputs):
        TestObject = backend_test_ingest(4)
        self.assertEqual(TestObject.algo_this_advisor.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(TestObject.algo_this_advisor.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(TestObject.algo_this_advisor.players["secret"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(TestObject.algo_this_advisor.players["Mia"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(TestObject.algo_this_advisor.players["Jane"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})

        prob = 1/(30-7)
        self.assertEqual(TestObject.algo_this_advisor.players["myself"].suspect_must_have, {"Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(TestObject.algo_this_advisor.players["Jane"].suspect_possibly_have, {"Mrs Peacock": 6/20, "Colonel Mustard": 6/20, 
        "Professor Plum":6/20, "Sgt. Gray": 6/20, "Monsieur Brunette": 6/20, "Mme. Rose": 6/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Michael"].suspect_possibly_have, {"Mrs Peacock": 5/20, "Colonel Mustard": 5/20, 
        "Professor Plum":5/20, "Sgt. Gray":5/20, "Monsieur Brunette":5/20, "Mme. Rose":5/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Mia"].suspect_possibly_have, {"Mrs Peacock": 6/20, "Colonel Mustard":6/20, 
        "Professor Plum":6/20, "Sgt. Gray":6/20, "Monsieur Brunette":6/20, "Mme. Rose":6/20})
        
        self.assertEqual(TestObject.algo_this_advisor.players["Jane"].weapon_possibly_have, {"Candlestick":6/20, "Knife":6/20, "Lead Pipe":6/20, 
        "Horseshoe":6/20, "Poison":6/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Michael"].weapon_possibly_have, {"Candlestick":5/20, "Knife":5/20, "Lead Pipe":5/20, 
        "Horseshoe":5/20, "Poison":5/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Mia"].weapon_possibly_have, {"Candlestick": 6/20, "Knife":6/20, "Lead Pipe":6/20, 
        "Horseshoe":6/20, "Poison":6/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Jane"].weapon_must_have, {"Revolver"})
        self.assertEqual(TestObject.algo_this_advisor.players["Mia"].weapon_must_not_have, {"Revolver","Rope", "Wrench"})
        self.assertEqual(TestObject.algo_this_advisor.players["Michael"].weapon_must_not_have, {"Revolver","Rope", "Wrench"})
        self.assertEqual(TestObject.algo_this_advisor.players["Jane"].weapon_must_not_have, {"Rope", "Wrench"})

        self.assertEqual(TestObject.algo_this_advisor.players["Jane"].room_possibly_have, {"Carriage House": 6/20, "Kitchen": 6/20, "Trophy Room": 6/20, 
        "Dining Room": 6/20, "Drawing Room": 6/20, "Courtyard": 6/20, "Fountain": 6/20, "Library": 6/20, "Billiard Room": 6/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Michael"].room_possibly_have, {"Carriage House": 5/20, "Kitchen": 5/20, "Trophy Room": 5/20, 
        "Dining Room": 5/20, "Drawing Room": 5/20, "Courtyard": 5/20, "Fountain": 5/20, "Library": 5/20, "Billiard Room": 5/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Mia"].room_possibly_have, {"Carriage House": 6/20, "Kitchen": 6/20, "Trophy Room": 6/20, 
        "Dining Room": 6/20, "Drawing Room": 6/20, "Courtyard": 6/20, "Fountain": 6/20, "Library": 6/20, "Billiard Room": 6/20})
        self.assertEqual(TestObject.algo_this_advisor.players["Mia"].room_must_have, {"Gazebo"})
        self.assertEqual(TestObject.algo_this_advisor.players["Mia"].room_must_not_have, {"Studio", "Conservatory"})
        self.assertEqual(TestObject.algo_this_advisor.players["Michael"].room_must_not_have, {"Studio", "Conservatory","Gazebo"})
        self.assertEqual(TestObject.algo_this_advisor.players["Jane"].room_must_not_have, {"Studio", "Conservatory","Gazebo"})


        self.assertEqual(TestObject.algo_this_advisor.players["secret"].suspect_possibly_have, {"Mrs Peacock": 1/6, "Colonel Mustard": 1/6, 
        "Professor Plum":1/6, "Sgt. Gray": 1/6, "Monsieur Brunette": 1/6, "Mme. Rose": 1/6})
        self.assertEqual(TestObject.algo_this_advisor.players["secret"].weapon_possibly_have, {"Candlestick":1/5, "Knife":1/5, "Lead Pipe":1/5, 
        "Horseshoe":1/5, "Poison":1/5})
        self.assertEqual(TestObject.algo_this_advisor.players["secret"].room_possibly_have, {"Carriage House": 1/9, "Kitchen": 1/9, "Trophy Room": 1/9, 
        "Dining Room": 1/9, "Drawing Room": 1/9, "Courtyard": 1/9, "Fountain": 1/9, "Library": 1/9, "Billiard Room": 1/9})


if __name__ == '__main__':
    unittest.main()