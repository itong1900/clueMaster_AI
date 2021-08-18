import unittest
import sys
sys.path.append("../main/")
from Advisor import Advisor

from unittest.mock import patch
from unittest import TestCase
import math
# from unittest.mock import Mock
#advisor1 = Advisor(4)


class TestAdvisor(unittest.TestCase):
    
    # Advisor 1
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

        prob = 1/(30-6)
        self.assertEqual(Advisor1.players["Mia"].suspect_possibly_have, {"Miss Scarlet": prob*7, "Mrs White":prob*7, "Mrs Peacock":prob*7, "Colonel Mustard":prob*7, 
        "Professor Plum":prob*7, "Sgt. Gray":prob*7, "Monsieur Brunette":prob*7, "Mme. Rose":prob*7})
        self.assertEqual(Advisor1.players["Mia"].weapon_possibly_have, {"Candlestick": prob*7, "Knife":prob*7, "Lead Pipe":prob*7, 
        "Revolver":prob*7, "Horseshoe":prob*7, "Poison":prob*7})
        self.assertEqual(Advisor1.players["Mia"].room_possibly_have, {"Carriage House":prob*7, "Kitchen":prob*7, "Trophy Room":prob*7, "Dining Room":prob*7, 
        "Drawing Room":prob*7, "Gazebo":prob*7, "Courtyard":prob*7, "Fountain":prob*7, "Library":prob*7, "Billiard Room":prob*7})

    # Advisor 2
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

        prob = 1/(30-7)
        self.assertEqual(Advisor2.players["Michael"].suspect_possibly_have, {"Sgt. Gray":prob*6, "Monsieur Brunette":prob*6, "Mme. Rose":prob*6})
        self.assertEqual(Advisor2.players["Michael"].weapon_possibly_have, {"Candlestick":prob*6, "Knife":prob*6, "Lead Pipe":prob*6, "Revolver":prob*6, 
        "Rope":prob*6, "Wrench":prob*6, "Horseshoe":prob*6, "Poison":prob*6})
        self.assertEqual(Advisor2.players["Michael"].room_possibly_have, {"Carriage House":prob*6, "Conservatory":prob*6, "Kitchen":prob*6, "Trophy Room":prob*6, 
        "Dining Room":prob*6, "Drawing Room":prob*6, "Gazebo":prob*6, "Courtyard":prob*6, "Fountain":prob*6, "Library":prob*6, "Billiard Room":prob*6, "Studio":prob*6})

        self.assertEqual(Advisor2.players["Jane"].suspect_possibly_have, {"Sgt. Gray":prob*7, "Monsieur Brunette":prob*7, "Mme. Rose":prob*7})

    # Advisor 3   
    # Game with 1 myself round
    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White", "Rope, Wrench", "Studio, Conservatory", "Mia, 7", "Michael, 6","Jane,7", 
    "Next turn", "myself", "Miss Peach, Revolver, Gazebo", "Michael, Jane, Mia", 
    "Query", "Player_Summary", "Jane", "Exit"])
    def test_Game3_setup(self, mock_inputs):
        Advisor3 = Advisor(4)
        self.assertEqual(Advisor3.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(Advisor3.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["secret"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["Mia"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["Jane"].suspect_must_not_have, {"Miss Peach", "Miss Scarlet", "Mr. Green", "Mrs White"})

        prob = 1/(30-7)
        self.assertEqual(Advisor3.players["myself"].suspect_must_have, {"Miss Scarlet", "Mr. Green", "Mrs White"})
        self.assertEqual(Advisor3.players["Jane"].suspect_possibly_have, {"Mrs Peacock": 6/20, "Colonel Mustard": 6/20, 
        "Professor Plum":6/20, "Sgt. Gray": 6/20, "Monsieur Brunette": 6/20, "Mme. Rose": 6/20})
        self.assertEqual(Advisor3.players["Michael"].suspect_possibly_have, {"Mrs Peacock": 5/20, "Colonel Mustard": 5/20, 
        "Professor Plum":5/20, "Sgt. Gray":5/20, "Monsieur Brunette":5/20, "Mme. Rose":5/20})
        self.assertEqual(Advisor3.players["Mia"].suspect_possibly_have, {"Mrs Peacock": 6/20, "Colonel Mustard":6/20, 
        "Professor Plum":6/20, "Sgt. Gray":6/20, "Monsieur Brunette":6/20, "Mme. Rose":6/20})
        
        self.assertEqual(Advisor3.players["Jane"].weapon_possibly_have, {"Candlestick":6/20, "Knife":6/20, "Lead Pipe":6/20, 
        "Horseshoe":6/20, "Poison":6/20})
        self.assertEqual(Advisor3.players["Michael"].weapon_possibly_have, {"Candlestick":5/20, "Knife":5/20, "Lead Pipe":5/20, 
        "Horseshoe":5/20, "Poison":5/20})
        self.assertEqual(Advisor3.players["Mia"].weapon_possibly_have, {"Candlestick": 6/20, "Knife":6/20, "Lead Pipe":6/20, 
        "Horseshoe":6/20, "Poison":6/20})
        self.assertEqual(Advisor3.players["Jane"].weapon_must_have, {"Revolver"})
        self.assertEqual(Advisor3.players["Mia"].weapon_must_not_have, {"Revolver","Rope", "Wrench"})
        self.assertEqual(Advisor3.players["Michael"].weapon_must_not_have, {"Revolver","Rope", "Wrench"})
        self.assertEqual(Advisor3.players["Jane"].weapon_must_not_have, {"Rope", "Wrench"})

        self.assertEqual(Advisor3.players["Jane"].room_possibly_have, {"Carriage House": 6/20, "Kitchen": 6/20, "Trophy Room": 6/20, 
        "Dining Room": 6/20, "Drawing Room": 6/20, "Courtyard": 6/20, "Fountain": 6/20, "Library": 6/20, "Billiard Room": 6/20})
        self.assertEqual(Advisor3.players["Michael"].room_possibly_have, {"Carriage House": 5/20, "Kitchen": 5/20, "Trophy Room": 5/20, 
        "Dining Room": 5/20, "Drawing Room": 5/20, "Courtyard": 5/20, "Fountain": 5/20, "Library": 5/20, "Billiard Room": 5/20})
        self.assertEqual(Advisor3.players["Mia"].room_possibly_have, {"Carriage House": 6/20, "Kitchen": 6/20, "Trophy Room": 6/20, 
        "Dining Room": 6/20, "Drawing Room": 6/20, "Courtyard": 6/20, "Fountain": 6/20, "Library": 6/20, "Billiard Room": 6/20})
        self.assertEqual(Advisor3.players["Mia"].room_must_have, {"Gazebo"})
        self.assertEqual(Advisor3.players["Mia"].room_must_not_have, {"Studio", "Conservatory"})
        self.assertEqual(Advisor3.players["Michael"].room_must_not_have, {"Studio", "Conservatory","Gazebo"})
        self.assertEqual(Advisor3.players["Jane"].room_must_not_have, {"Studio", "Conservatory","Gazebo"})


        self.assertEqual(Advisor3.players["secret"].suspect_possibly_have, {"Mrs Peacock": 1/6, "Colonel Mustard": 1/6, 
        "Professor Plum":1/6, "Sgt. Gray": 1/6, "Monsieur Brunette": 1/6, "Mme. Rose": 1/6})
        self.assertEqual(Advisor3.players["secret"].weapon_possibly_have, {"Candlestick":1/5, "Knife":1/5, "Lead Pipe":1/5, 
        "Horseshoe":1/5, "Poison":1/5})
        self.assertEqual(Advisor3.players["secret"].room_possibly_have, {"Carriage House": 1/9, "Kitchen": 1/9, "Trophy Room": 1/9, 
        "Dining Room": 1/9, "Drawing Room": 1/9, "Courtyard": 1/9, "Fountain": 1/9, "Library": 1/9, "Billiard Room": 1/9})

    # Advisor 4
    # a more complete game with clear road maps and a few myself turns with 3/2/1 cards given, include a rebalance test to secret agent.
    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White", "Candlestick, Knife", "Carriage House, Conservatory","Mia, 7", "Michael, 6","Jane,7",
    "Next turn", "myself", "Mrs Peacock, Rope, Library", "Mia, Michael, Jane",
    "Next turn", "myself", "Miss Peach, Horseshoe ,Gazebo", "Michael, Jane, None",
    "Next turn", "myself", "Mme. Rose, Poison, Gazebo", "None, None, Michael", 
    "Query", "Player_Summary", "Michael", "Exit"])
    def test_Game4(self, mock_inputs):
        Advisor4 = Advisor(4) 

        self.assertEqual(Advisor4.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(Advisor4.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock"})
        self.assertEqual(Advisor4.players["Michael"].suspect_possibly_have, {"Colonel Mustard": 3/17, "Professor Plum": 3/17, 
        "Sgt. Gray": 3/17, "Monsieur Brunette": 3/17, "Mme. Rose":  1/2})
        self.assertEqual(Advisor4.players["Michael"].weapon_must_have, {"Rope"})
        self.assertEqual(Advisor4.players["Michael"].weapon_must_not_have, {"Candlestick", "Knife", "Horseshoe"})
        self.assertEqual(Advisor4.players["Michael"].weapon_possibly_have, {"Lead Pipe": 3/17, "Revolver": 3/17,
        "Wrench": 3/17, "Poison": 1/2})
        self.assertEqual(Advisor4.players["Michael"].room_must_have, {"Gazebo"})
        self.assertEqual(Advisor4.players["Michael"].room_must_not_have, {"Carriage House", "Conservatory", "Library"})
        self.assertEqual(Advisor4.players["Michael"].room_possibly_have, {"Kitchen": 3/17, "Trophy Room": 3/17, "Dining Room": 3/17, 
        "Drawing Room": 3/17, "Courtyard": 3/17, "Fountain": 3/17, "Billiard Room": 3/17, "Studio": 3/17})

        self.assertEqual(Advisor4.players["Jane"].suspect_must_have,set())
        self.assertEqual(Advisor4.players["Jane"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Miss Peach", 
        "Mme. Rose"})
        self.assertEqual(Advisor4.players["Jane"].suspect_possibly_have, {"Colonel Mustard":5/15, "Professor Plum": 5/15, 
        "Sgt. Gray": 5/15, "Monsieur Brunette": 5/15})
        self.assertEqual(Advisor4.players["Jane"].weapon_must_have, {"Horseshoe"})
        self.assertEqual(Advisor4.players["Jane"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Poison"})
        self.assertEqual(Advisor4.players["Jane"].weapon_possibly_have, {"Lead Pipe": 5/15, "Revolver": 5/15, "Wrench": 5/15 })
        self.assertEqual(Advisor4.players["Jane"].room_must_have, {"Library"})
        self.assertEqual(Advisor4.players["Jane"].room_must_not_have, {"Carriage House", "Conservatory", "Gazebo"})
        self.assertEqual(Advisor4.players["Jane"].room_possibly_have, {"Kitchen": 5/15, "Trophy Room":5/15, "Dining Room":5/15, 
        "Drawing Room":5/15, "Courtyard":5/15, "Fountain":5/15, "Billiard Room":5/15, "Studio":5/15})
                                                                        
        self.assertEqual(Advisor4.players["Mia"].suspect_must_have,{"Mrs Peacock"})
        self.assertEqual(Advisor4.players["Mia"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Miss Peach", "Mme. Rose"})
        self.assertEqual(Advisor4.players["Mia"].suspect_possibly_have, {"Colonel Mustard": 6/15, "Professor Plum": 6/15, 
        "Sgt. Gray": 6/15, "Monsieur Brunette": 6/15})
        self.assertEqual(Advisor4.players["Mia"].weapon_must_have, set())
        self.assertEqual(Advisor4.players["Mia"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Horseshoe", "Poison"})
        self.assertEqual(Advisor4.players["Mia"].weapon_possibly_have, {"Lead Pipe": 6/15, "Revolver":6/15, "Wrench":6/15})
        self.assertEqual(Advisor4.players["Mia"].room_must_have, set())
        self.assertEqual(Advisor4.players["Mia"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Gazebo"})
        self.assertEqual(Advisor4.players["Mia"].room_possibly_have, {"Kitchen": 6/15, "Trophy Room":6/15, "Dining Room":6/15, 
        "Drawing Room":6/15, "Courtyard":6/15, "Fountain":6/15, "Billiard Room":6/15, "Studio":6/15})

        self.assertEqual(Advisor4.players["secret"].suspect_must_have,set())
        self.assertEqual(Advisor4.players["secret"].suspect_must_not_have,{"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Miss Peach"})
        self.assertEqual(Advisor4.players["secret"].suspect_possibly_have, {"Colonel Mustard": 1/5, "Professor Plum": 1/5, 
        "Sgt. Gray": 1/5, "Monsieur Brunette": 1/5, "Mme. Rose": 1/2})

        self.assertEqual(Advisor4.players["secret"].weapon_must_have,set())
        self.assertEqual(Advisor4.players["secret"].weapon_must_not_have,{"Candlestick", "Knife", "Rope", "Horseshoe"})
        self.assertEqual(Advisor4.players["secret"].weapon_possibly_have, {"Lead Pipe": 1/4, "Revolver": 1/4, "Wrench": 1/4, 
        "Poison": max(1/4, 1/2)})

        self.assertEqual(Advisor4.players["secret"].room_must_have,set())
        self.assertEqual(Advisor4.players["secret"].room_must_not_have,{"Carriage House", "Conservatory", "Library", "Gazebo"})
        self.assertEqual(Advisor4.players["secret"].room_possibly_have, {"Kitchen": 1/8, "Trophy Room": 1/8, "Dining Room": 1/8, "Drawing Room": 1/8, 
        "Courtyard": 1/8, "Fountain": 1/8, "Billiard Room": 1/8, "Studio": 1/8})


    # Advisor 5
    # similar to Game4, but add a round to test hacking to suspect and weapon, also test on the straighforward inference
    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White", "Candlestick, Knife", "Carriage House, Conservatory","Mia, 7", "Michael, 6","Jane,7",
    "Next turn", "myself", "Mrs Peacock, Rope, Library", "Mia, Michael, Jane",
    "Next turn", "myself", "Miss Peach, Horseshoe ,Gazebo", "Michael, Jane, None",
    "Next turn", "myself", "Mme. Rose, Poison, Gazebo", "None, None, Michael", 
    "Next turn", "myself", "Mme. Rose, Poison, Kitchen", "None, None, Mia",
    "Query", "Player_Summary", "secret", "Exit"])
    def test_Game5(self, mock_inputs):
        Advisor5 = Advisor(4)
        
        self.assertEqual(Advisor5.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(Advisor5.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock","Mme. Rose"})
        self.assertEqual(Advisor5.players["Michael"].suspect_possibly_have, {"Colonel Mustard": 3/14, "Professor Plum": 3/14, 
        "Sgt. Gray": 3/14, "Monsieur Brunette": 3/14})
        self.assertEqual(Advisor5.players["Michael"].weapon_must_have, {"Rope"})
        self.assertEqual(Advisor5.players["Michael"].weapon_must_not_have, {"Candlestick", "Knife", "Horseshoe", "Poison"})
        self.assertEqual(Advisor5.players["Michael"].weapon_possibly_have, {"Lead Pipe": 3/14, "Revolver": 3/14,
        "Wrench": 3/14})
        self.assertEqual(Advisor5.players["Michael"].room_must_have, {"Gazebo"})
        self.assertEqual(Advisor5.players["Michael"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Kitchen"})
        self.assertEqual(Advisor5.players["Michael"].room_possibly_have, {"Trophy Room": 3/14, "Dining Room": 3/14, 
        "Drawing Room": 3/14, "Courtyard": 3/14, "Fountain": 3/14, "Billiard Room": 3/14, "Studio": 3/14})

        self.assertEqual(Advisor5.players["Jane"].suspect_must_have,set())
        self.assertEqual(Advisor5.players["Jane"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Miss Peach", 
        "Mme. Rose"})
        self.assertEqual(Advisor5.players["Jane"].suspect_possibly_have, {"Colonel Mustard":5/14, "Professor Plum":5/14, 
        "Sgt. Gray": 5/14, "Monsieur Brunette": 5/14})
        self.assertEqual(Advisor5.players["Jane"].weapon_must_have, {"Horseshoe"})
        self.assertEqual(Advisor5.players["Jane"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Poison"})
        self.assertEqual(Advisor5.players["Jane"].weapon_possibly_have, {"Lead Pipe": 5/14, "Revolver": 5/14, "Wrench": 5/14 })
        self.assertEqual(Advisor5.players["Jane"].room_must_have, {"Library"})
        self.assertEqual(Advisor5.players["Jane"].room_must_not_have, {"Carriage House", "Conservatory", "Gazebo", "Kitchen"})
        self.assertEqual(Advisor5.players["Jane"].room_possibly_have, {"Trophy Room":5/14, "Dining Room":5/14, 
        "Drawing Room":5/14, "Courtyard":5/14, "Fountain":5/14, "Billiard Room":5/14, "Studio":5/14})
                                                                        
        self.assertEqual(Advisor5.players["Mia"].suspect_must_have,{"Mrs Peacock"})
        self.assertEqual(Advisor5.players["Mia"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Miss Peach", "Mme. Rose"})
        self.assertEqual(Advisor5.players["Mia"].suspect_possibly_have, {"Colonel Mustard": 5/14, "Professor Plum": 5/14, 
        "Sgt. Gray": 5/14, "Monsieur Brunette": 5/14})
        self.assertEqual(Advisor5.players["Mia"].weapon_must_have, set())
        self.assertEqual(Advisor5.players["Mia"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Horseshoe", "Poison"})
        self.assertEqual(Advisor5.players["Mia"].weapon_possibly_have, {"Lead Pipe": 5/14, "Revolver":5/14, "Wrench":5/14})
        self.assertEqual(Advisor5.players["Mia"].room_must_have, {"Kitchen"})
        self.assertEqual(Advisor5.players["Mia"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Gazebo"})
        self.assertEqual(Advisor5.players["Mia"].room_possibly_have, {"Trophy Room":5/14, "Dining Room":5/14, 
        "Drawing Room":5/14, "Courtyard":5/14, "Fountain":5/14, "Billiard Room":5/14, "Studio":5/14})

        self.assertEqual(Advisor5.players["secret"].suspect_must_have,{"Mme. Rose"})
        self.assertEqual(Advisor5.players["secret"].suspect_must_not_have,{"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", 
        "Colonel Mustard", "Professor Plum", "Miss Peach", "Sgt. Gray", "Monsieur Brunette"})
        self.assertEqual(Advisor5.players["secret"].suspect_possibly_have,{})
        self.assertEqual(Advisor5.players["secret"].weapon_must_have,{"Poison"})
        self.assertEqual(Advisor5.players["secret"].weapon_must_not_have,{"Candlestick", "Knife", "Lead Pipe", "Revolver", "Rope", 
        "Wrench", "Horseshoe"})
        self.assertEqual(Advisor5.players["secret"].weapon_possibly_have,{})
        self.assertEqual(Advisor5.players["secret"].room_must_have,set())
        self.assertEqual(Advisor5.players["secret"].room_must_not_have,{'Library', 'Gazebo', 'Conservatory', 'Kitchen', 'Carriage House'})
        self.assertEqual(Advisor5.players["secret"].room_possibly_have,{"Trophy Room": 1/7, "Dining Room": 1/7, "Drawing Room": 1/7, 
        "Courtyard": 1/7, "Fountain": 1/7, "Billiard Room": 1/7, "Studio": 1/7})
        

    
    # Advisor 6
    # Parellel to Advisor5, last turn vary, test the one step forard and score changes
    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White", "Candlestick, Knife", "Carriage House, Conservatory","Mia, 7", "Michael, 6","Jane,7",
    "Next turn", "myself", "Mrs Peacock, Rope, Library", "Mia, Michael, Jane",
    "Next turn", "myself", "Miss Peach, Horseshoe ,Gazebo", "Michael, Jane, None",
    "Next turn", "myself", "Mme. Rose, Poison, Gazebo", "None, None, Michael", 
    "Next turn", "myself", "Mme. Rose, Poison, Drawing Room", "None, None, Michael",
    #"Query", "Log", "Exit"])
    # "Next turn", "Michael", "Professor Plum, Revolver, Fountain", "Mia, Jane",
    "Query","Log","Exit"])
    def test_Game6(self, mock_inputs):
        Advisor6 = Advisor(4)

        self.assertEqual(Advisor6.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(Advisor6.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock"})
        self.assertEqual(Advisor6.players["Michael"].suspect_possibly_have, {"Colonel Mustard": 2/16, "Professor Plum": 2/16, 
        "Sgt. Gray": 2/16, "Monsieur Brunette": 2/16,"Mme. Rose":1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor6.players["Michael"].weapon_must_have, {"Rope"})
        self.assertEqual(Advisor6.players["Michael"].weapon_must_not_have, {"Candlestick", "Knife", "Horseshoe"})
        self.assertEqual(Advisor6.players["Michael"].weapon_possibly_have, {"Lead Pipe": 2/16, "Revolver": 2/16,
        "Wrench": 2/16, "Poison": 1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor6.players["Michael"].room_must_have, {"Gazebo", "Drawing Room"})
        self.assertEqual(Advisor6.players["Michael"].room_must_not_have, {"Carriage House", "Conservatory", "Library"})
        self.assertEqual(Advisor6.players["Michael"].room_possibly_have, {"Kitchen": 2/16, "Trophy Room": 2/16, "Dining Room": 2/16, 
        "Courtyard": 2/16, "Fountain": 2/16, "Billiard Room": 2/16, "Studio": 2/16})

        self.assertEqual(Advisor6.players["Jane"].suspect_must_have,set())
        self.assertEqual(Advisor6.players["Jane"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Miss Peach", 
        "Mme. Rose"})
        self.assertEqual(Advisor6.players["Jane"].suspect_possibly_have, {"Colonel Mustard":5/14, "Professor Plum":5/14, 
        "Sgt. Gray": 5/14, "Monsieur Brunette": 5/14})
        self.assertEqual(Advisor6.players["Jane"].weapon_must_have, {"Horseshoe"})
        self.assertEqual(Advisor6.players["Jane"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Poison"})
        self.assertEqual(Advisor6.players["Jane"].weapon_possibly_have, {"Lead Pipe": 5/14, "Revolver": 5/14, "Wrench": 5/14 })
        self.assertEqual(Advisor6.players["Jane"].room_must_have, {"Library"})
        self.assertEqual(Advisor6.players["Jane"].room_must_not_have, {"Carriage House", "Conservatory", "Gazebo", "Drawing Room"})
        self.assertEqual(Advisor6.players["Jane"].room_possibly_have, {"Kitchen":5/14, "Trophy Room":5/14, "Dining Room":5/14, 
        "Courtyard":5/14, "Fountain":5/14, "Billiard Room":5/14, "Studio":5/14})
                                                                        
        self.assertEqual(Advisor6.players["Mia"].suspect_must_have,{"Mrs Peacock"})
        self.assertEqual(Advisor6.players["Mia"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Miss Peach", "Mme. Rose"})
        self.assertEqual(Advisor6.players["Mia"].suspect_possibly_have, {"Colonel Mustard": 6/14, "Professor Plum": 6/14, 
        "Sgt. Gray": 6/14, "Monsieur Brunette": 6/14})
        self.assertEqual(Advisor6.players["Mia"].weapon_must_have, set())
        self.assertEqual(Advisor6.players["Mia"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Horseshoe", "Poison"})
        self.assertEqual(Advisor6.players["Mia"].weapon_possibly_have, {"Lead Pipe": 6/14, "Revolver":6/14, "Wrench":6/14})
        self.assertEqual(Advisor6.players["Mia"].room_must_have, set())
        self.assertEqual(Advisor6.players["Mia"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Gazebo","Drawing Room"})
        self.assertEqual(Advisor6.players["Mia"].room_possibly_have, {"Kitchen":6/14, "Trophy Room":6/14, "Dining Room":6/14, 
        "Courtyard":6/14, "Fountain":6/14, "Billiard Room":6/14, "Studio":6/14})

        self.assertEqual(Advisor6.players["secret"].suspect_must_have,set())
        self.assertEqual(Advisor6.players["secret"].suspect_must_not_have,{"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", 
        "Miss Peach"})
        self.assertEqual(Advisor6.players["secret"].suspect_possibly_have,{"Colonel Mustard":1/5, "Professor Plum":1/5, "Sgt. Gray":1/5, 
        "Monsieur Brunette":1/5, "Mme. Rose":1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor6.players["secret"].weapon_must_have,set())
        self.assertEqual(Advisor6.players["secret"].weapon_must_not_have,{"Candlestick", "Knife", "Rope", "Horseshoe"})
        self.assertEqual(Advisor6.players["secret"].weapon_possibly_have,{"Lead Pipe": 1/4, "Revolver": 1/4, "Wrench": 1/4,
        "Poison":1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor6.players["secret"].room_must_have,set())
        self.assertEqual(Advisor6.players["secret"].room_must_not_have,{"Carriage House", "Conservatory", "Library", "Gazebo", "Drawing Room"})
        self.assertEqual(Advisor6.players["secret"].room_possibly_have,{"Kitchen": 1/7, "Trophy Room": 1/7, "Dining Room": 1/7, 
        "Courtyard": 1/7, "Fountain": 1/7, "Billiard Room": 1/7, "Studio": 1/7})


    # Advisor 7
    # Inherit Advisor6, to validate the magnifier checkmethod
    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White", "Candlestick, Knife", "Carriage House, Conservatory","Mia, 7", "Michael, 6","Jane,7",
    "Next turn", "myself", "Mrs Peacock, Rope, Library", "Mia, Michael, Jane",
    "Next turn", "myself", "Miss Peach, Horseshoe ,Gazebo", "Michael, Jane, None",
    "Next turn", "myself", "Mme. Rose, Poison, Gazebo", "None, None, Michael", 
    "Next turn", "myself", "Mme. Rose, Poison, Drawing Room", "None, None, Michael",
    "Magnifier", "Mia, Kitchen",
    "Magnifier", "Jane, Horseshoe",
    "Query","Log","Exit"])
    def test_Game7(self, mock_inputs):
        Advisor7 = Advisor(4)

        self.assertEqual(Advisor7.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(Advisor7.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock"})
        self.assertEqual(Advisor7.players["Michael"].suspect_possibly_have, {"Colonel Mustard": 2/15, "Professor Plum": 2/15, 
        "Sgt. Gray": 2/15, "Monsieur Brunette": 2/15,"Mme. Rose":1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor7.players["Michael"].weapon_must_have, {"Rope"})
        self.assertEqual(Advisor7.players["Michael"].weapon_must_not_have, {"Candlestick", "Knife", "Horseshoe"})
        self.assertEqual(Advisor7.players["Michael"].weapon_possibly_have, {"Lead Pipe": 2/15, "Revolver": 2/15,
        "Wrench": 2/15, "Poison": 1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor7.players["Michael"].room_must_have, {"Gazebo", "Drawing Room"})
        self.assertEqual(Advisor7.players["Michael"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Kitchen"})
        self.assertEqual(Advisor7.players["Michael"].room_possibly_have, {"Trophy Room": 2/15, "Dining Room": 2/15, 
        "Courtyard": 2/15, "Fountain": 2/15, "Billiard Room": 2/15, "Studio": 2/15})

        self.assertEqual(Advisor7.players["Jane"].suspect_must_have,set())
        self.assertEqual(Advisor7.players["Jane"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Miss Peach", 
        "Mme. Rose"})
        self.assertEqual(Advisor7.players["Jane"].suspect_possibly_have, {"Colonel Mustard":5/13, "Professor Plum":5/13, 
        "Sgt. Gray": 5/13, "Monsieur Brunette": 5/13})
        self.assertEqual(Advisor7.players["Jane"].weapon_must_have, {"Horseshoe"})
        self.assertEqual(Advisor7.players["Jane"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Poison"})
        self.assertEqual(Advisor7.players["Jane"].weapon_possibly_have, {"Lead Pipe": 5/13, "Revolver": 5/13, "Wrench": 5/13 })
        self.assertEqual(Advisor7.players["Jane"].room_must_have, {"Library"})
        self.assertEqual(Advisor7.players["Jane"].room_must_not_have, {"Carriage House", "Conservatory", "Gazebo", "Drawing Room", "Kitchen"})
        self.assertEqual(Advisor7.players["Jane"].room_possibly_have, {"Trophy Room":5/13, "Dining Room":5/13, 
        "Courtyard":5/13, "Fountain":5/13, "Billiard Room":5/13, "Studio":5/13})
                                                                        
        self.assertEqual(Advisor7.players["Mia"].suspect_must_have,{"Mrs Peacock"})
        self.assertEqual(Advisor7.players["Mia"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Miss Peach", "Mme. Rose"})
        self.assertEqual(Advisor7.players["Mia"].suspect_possibly_have, {"Colonel Mustard": 5/13, "Professor Plum": 5/13, 
        "Sgt. Gray": 5/13, "Monsieur Brunette": 5/13})
        self.assertEqual(Advisor7.players["Mia"].weapon_must_have, set())
        self.assertEqual(Advisor7.players["Mia"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Horseshoe", "Poison"})
        self.assertEqual(Advisor7.players["Mia"].weapon_possibly_have, {"Lead Pipe": 5/13, "Revolver":5/13, "Wrench":5/13})
        self.assertEqual(Advisor7.players["Mia"].room_must_have, {"Kitchen"})
        self.assertEqual(Advisor7.players["Mia"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Gazebo","Drawing Room"})
        self.assertEqual(Advisor7.players["Mia"].room_possibly_have, {"Trophy Room":5/13, "Dining Room":5/13, 
        "Courtyard":5/13, "Fountain":5/13, "Billiard Room":5/13, "Studio":5/13})

        self.assertEqual(Advisor7.players["secret"].suspect_must_have,set())
        self.assertEqual(Advisor7.players["secret"].suspect_must_not_have,{"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", 
        "Miss Peach"})
        self.assertEqual(Advisor7.players["secret"].suspect_possibly_have,{"Colonel Mustard":1/5, "Professor Plum":1/5, "Sgt. Gray":1/5, 
        "Monsieur Brunette":1/5, "Mme. Rose":1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor7.players["secret"].weapon_must_have,set())
        self.assertEqual(Advisor7.players["secret"].weapon_must_not_have,{"Candlestick", "Knife", "Rope", "Horseshoe"})
        self.assertEqual(Advisor7.players["secret"].weapon_possibly_have,{"Lead Pipe": 1/4, "Revolver": 1/4, "Wrench": 1/4,
        "Poison":1/2 + math.log(3/2, 5)})
        self.assertEqual(Advisor7.players["secret"].room_must_have,set())
        self.assertEqual(Advisor7.players["secret"].room_must_not_have,{"Carriage House", "Conservatory", "Library", 
        "Kitchen", "Gazebo", "Drawing Room"})
        self.assertEqual(Advisor7.players["secret"].room_possibly_have,{"Trophy Room": 1/6, "Dining Room": 1/6, 
        "Courtyard": 1/6, "Fountain": 1/6, "Billiard Room": 1/6, "Studio": 1/6})


    

    # Adivisor 8
    # Inherit Advisor4, to validate the otherAgent turn 3 cardgivers with 1 in must-have case, also test a 3 must-have case which do nothing
    @patch("builtins.input", side_effect = ["7", "Miss Scarlet, Mr. Green, Mrs White", "Candlestick, Knife", "Carriage House, Conservatory","Mia, 7", "Michael, 6","Jane,7",
    "Next turn", "myself", "Mrs Peacock, Rope, Library", "Mia, Michael, Jane",
    "Next turn", "myself", "Miss Peach, Horseshoe ,Gazebo", "Michael, Jane, None",
    "Next turn", "myself", "Mme. Rose, Poison, Gazebo", "None, None, Michael", 
    "Next turn", "Michael", "Mrs White, Lead Pipe, Fountain", "myself, Mia, Jane",
    "Next turn", "Jane", "Mrs Peacock, Rope, Conservatory", "Mia, Michael, myself",
    "Query","Player_Summary","Michael","Exit"])
    def test_Game8(self, mock_inputs):
        Advisor8 = Advisor(4)

        self.assertEqual(Advisor8.players["Michael"].suspect_must_have, {"Miss Peach"})
        self.assertEqual(Advisor8.players["Michael"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock"})
        self.assertEqual(Advisor8.players["Michael"].suspect_possibly_have, {"Colonel Mustard": 3/15, "Professor Plum": 3/15, 
        "Sgt. Gray": 3/15, "Monsieur Brunette": 3/15,"Mme. Rose":1/2})
        self.assertEqual(Advisor8.players["Michael"].weapon_must_have, {"Rope"})
        self.assertEqual(Advisor8.players["Michael"].weapon_must_not_have, {"Candlestick", "Knife", "Horseshoe", "Lead Pipe"})
        self.assertEqual(Advisor8.players["Michael"].weapon_possibly_have, {"Revolver": 3/15,
        "Wrench": 3/15, "Poison": 1/2})
        self.assertEqual(Advisor8.players["Michael"].room_must_have, {"Gazebo"})
        self.assertEqual(Advisor8.players["Michael"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Fountain"})
        self.assertEqual(Advisor8.players["Michael"].room_possibly_have, {"Kitchen": 3/15, "Trophy Room": 3/15, "Dining Room": 3/15, 
        "Drawing Room": 3/15, "Courtyard": 3/15, "Billiard Room": 3/15, "Studio": 3/15})

        self.assertEqual(Advisor8.players["Jane"].suspect_must_have,set())
        self.assertEqual(Advisor8.players["Jane"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Miss Peach", 
        "Mme. Rose"})
        self.assertEqual(Advisor8.players["Jane"].suspect_possibly_have, {"Colonel Mustard":5/15, "Professor Plum": 5/15, 
        "Sgt. Gray": 5/15, "Monsieur Brunette": 5/15})
        self.assertEqual(Advisor8.players["Jane"].weapon_must_have, {"Horseshoe"})
        self.assertEqual(Advisor8.players["Jane"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Poison"})
        self.assertEqual(Advisor8.players["Jane"].weapon_possibly_have, {"Lead Pipe": 1/2, "Revolver": 5/15, "Wrench": 5/15 })
        self.assertEqual(Advisor8.players["Jane"].room_must_have, {"Library"})
        self.assertEqual(Advisor8.players["Jane"].room_must_not_have, {"Carriage House", "Conservatory", "Gazebo"})
        self.assertEqual(Advisor8.players["Jane"].room_possibly_have, {"Kitchen": 5/15, "Trophy Room":5/15, "Dining Room":5/15, 
        "Drawing Room":5/15, "Courtyard":5/15, "Fountain":1/2, "Billiard Room":5/15, "Studio":5/15})
                                                                        
        self.assertEqual(Advisor8.players["Mia"].suspect_must_have,{"Mrs Peacock"})
        self.assertEqual(Advisor8.players["Mia"].suspect_must_not_have, {"Miss Scarlet", "Mr. Green", "Mrs White", "Miss Peach", "Mme. Rose"})
        self.assertEqual(Advisor8.players["Mia"].suspect_possibly_have, {"Colonel Mustard": 6/15, "Professor Plum": 6/15, 
        "Sgt. Gray": 6/15, "Monsieur Brunette": 6/15})
        self.assertEqual(Advisor8.players["Mia"].weapon_must_have, set())
        self.assertEqual(Advisor8.players["Mia"].weapon_must_not_have, {"Candlestick", "Knife", "Rope", "Horseshoe", "Poison"})
        self.assertEqual(Advisor8.players["Mia"].weapon_possibly_have, {"Lead Pipe": 1/2, "Revolver":6/15, "Wrench":6/15})
        self.assertEqual(Advisor8.players["Mia"].room_must_have, set())
        self.assertEqual(Advisor8.players["Mia"].room_must_not_have, {"Carriage House", "Conservatory", "Library", "Gazebo"})
        self.assertEqual(Advisor8.players["Mia"].room_possibly_have, {"Kitchen": 6/15, "Trophy Room":6/15, "Dining Room":6/15, 
        "Drawing Room":6/15, "Courtyard":6/15, "Fountain":1/2, "Billiard Room":6/15, "Studio":6/15})

        self.assertEqual(Advisor8.players["secret"].suspect_must_have,set())
        self.assertEqual(Advisor8.players["secret"].suspect_must_not_have,{"Miss Scarlet", "Mr. Green", "Mrs White", "Mrs Peacock", "Miss Peach"})
        self.assertEqual(Advisor8.players["secret"].suspect_possibly_have, {"Colonel Mustard": 1/5, "Professor Plum": 1/5, 
        "Sgt. Gray": 1/5, "Monsieur Brunette": 1/5, "Mme. Rose": 1/2})

        self.assertEqual(Advisor8.players["secret"].weapon_must_have,set())
        self.assertEqual(Advisor8.players["secret"].weapon_must_not_have,{"Candlestick", "Knife", "Rope", "Horseshoe","Lead Pipe"})
        self.assertEqual(Advisor8.players["secret"].weapon_possibly_have, {"Revolver": 1/3, "Wrench": 1/3, 
        "Poison": max(1/3, 1/2)})

        self.assertEqual(Advisor8.players["secret"].room_must_have,set())
        self.assertEqual(Advisor8.players["secret"].room_must_not_have,{"Carriage House", "Conservatory", "Library", "Gazebo","Fountain"})
        self.assertEqual(Advisor8.players["secret"].room_possibly_have, {"Kitchen": 1/7, "Trophy Room": 1/7, "Dining Room": 1/7, "Drawing Room": 1/7, 
        "Courtyard": 1/7, "Billiard Room": 1/7, "Studio": 1/7})


if __name__ == '__main__':
    unittest.main()