from senpy import notify_me
import unittest

class TestNotifyMe(unittest.TestCase):

    def testUsualCall(self):
        notify_me("Notification Test")
        
    def testDefaultArgument(self):
        notify_me()

if __name__ == '__main__':
    unittest.main()
