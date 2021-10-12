import unittest
import sys

#from main.Simulator import Simulator
sys.path.append("../main/")
from Advisor import Advisor
from Simulator import Simulator

from unittest.mock import patch
from unittest import TestCase
import math


class TestSimulator(unittest.TestCase):
    # Advisor 1
    #@patch("builtins.input", side_effect = [5])
    def test_Game1_setup(self):
        print()
        Simulator1 = Simulator()