import unittest

class TestProject(unittest.TestCase):
    path = '../examples/qoob.exe'

    def test_file_not_found(self):
        self.ex