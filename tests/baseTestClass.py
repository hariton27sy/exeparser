import unittest
import os


class BaseTestClass(unittest.TestCase):
    def setUp(self):
        self.currPath = os.path.abspath(os.path.curdir)
        if os.path.split(self.currPath)[-1] == 'tests':
            os.chdir('../')
        if os.path.exists('exe_parser'):
            os.chdir('exe_parser')
        if os.path.exists('exeparser2'):
            os.chdir('exeparser2')
        elif os.path.exists('exeparser'):
            os.chdir('exeparser')

    def tearDown(self):
        os.chdir(self.currPath)
