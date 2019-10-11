import os
import sys
import unittest

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
import CLI.cli as c


class TestCLIMethods(unittest.TestCase):
    def test_formatted_output(self):
        pass