import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from senpy import notify_me
import unittest

class TestNotifyMe(unittest.TestCase):

    def testUsualCall(self):
        notify_me("Notification Test")
        

if __name__ == '__main__':
    unittest.main()
