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

    def test_Game2_setup(self):
        Simulator1 = Simulator(5)



if __name__ == '__main__':
    unittest.main()