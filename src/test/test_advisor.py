import unittest
import sys
sys.path.append("../main/")
from Advisor import Advisor

#advisor1 = Advisor(4)


class TestAdvisor(unittest.TestCase):
    
    def test_init_setup_methods(self):
        Advisor1 = Advisor(4)


if __name__ == '__main__':
    unittest.main()