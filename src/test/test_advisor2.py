import unittest
import sys
sys.path.append("../main/")
from Advisor import Advisor

from unittest.mock import patch
from unittest import TestCase
import math

class TestAdvisor2(unittest.TestCase):
    # Adivisor 17, if I follow suggestion closely in every myself turn 
    @patch("builtins.input", side_effect = ["7", "Miss Peach", "Rope", "Carriage House, Courtyard, Studio, Billiard Room, Dining Room","Michael, 6", "Yuan, 7","Nan, 7",
    "Next turn", "Yuan", "Miss Peach, Rope, Trophy Room", "myself",
    "Next turn", "Nan", "Professor Plum, Revolver, Studio", "Yuan, myself",
    "Next turn", "myself", "Professor Plum, Revolver, Dining Room", "Yuan, None, myself", 
    "Next turn", "Michael", "Professor Plum, Revolver, Courtyard", "Yuan, myself",
    "Next turn", "Yuan", "Professor Plum, Revolver, Conservatory", "Nan",
    "Next turn", "Nan", "Monsieur Brunette, Revolver, Conservatory", "Yuan",
    "Magnifier", "Nan, Conservatory",
    "Next turn", "myself", "Monsieur Brunette, Revolver, Kitchen", "Yuan, None, None", 
    "Next turn", "Michael", "Monsieur Brunette, Wrench, Billiard Room", "Yuan, myself",
    "Next turn", "Yuan", "Miss Peach, Revolver, Trophy Room", "myself",
    "Next turn", "myself", "Mrs White, Revolver, Library", "Nan, None, Michael",
    "Next turn", "Michael", "Miss Scarlet, Revolver, Studio", "Nan, myself",
    "Next turn", "Yuan", "Mme. Rose, Poison, Studio", "Nan, Michael, myself",
    "Next turn", "Nan", "Miss Peach, Knife, Billiard Room", "Michael, myself",
    "Next turn", "myself", "Miss Scarlet, Knife, Trophy Room", "None, Nan, None",
    "Next turn", "Michael", "Mrs White, Revolver, Conservatory", "Nan",
    "Next turn", "Yuan", "Sgt. Gray, Revolver, Conservatory", "Nan",
    "Magnifier", "Michael, Horseshoe",
    "Next turn", "myself", "Miss Scarlet, Lead Pipe, Studio", "Nan, Michael, myself",
    "Next turn", "Michael", "Mrs White, Knife, Drawing Room", "Nan, Yuan",
    "Next turn", "Yuan", "Mrs Peacock, Knife, Drawing Room", "Nan, Michael",
    "Next turn", "Nan", "Mrs White, Knife, Courtyard", "myself",
    "Next turn", "myself", "Sgt. Gray, Candlestick, Drawing Room", "Nan, None, Yuan",
    "Next turn", "Michael", "Mr. Green, Candlestick, Dinning Room", "myself, Yuan",
    "Next turn", "Nan", "Mr. Green, Poison, Dinning Room", "myself",
    "Suggestion", 
    "Magnifier", "Michael, Library", "Exit"])
    #"ScoreExport", "Game17","Exit"])
    # "Next turn", "myself", "Mrs Peacock, Wrench, Fountain", "Michael, Yuan, Nan",
    # "Next turn", "Yuan", "Mr. Green, Lead Pipe, Dinning Room", "Michael, myself",
    # #"Query", "Log", "Exit"])
    #"Query", "Player_Summary","secret","Exit"])
    def test_Game_17(self, mock_inputs):
        Advisor17 = Advisor(4)


if __name__ == '__main__':
    unittest.main()