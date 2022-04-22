import unittest
import main
import os

# For all tests to work set the environment variable CFDDNS_API_TOKEN via your profile or .env file

class TestMain(unittest.TestCase):
    @classmethod
    def setUp(self) -> None:
        self.ip = main.ip()

    def test_getcurrentip(self):
        self.assertIsInstance(self.ip.getcurrentip(), str)
    
    def test_updatepersist(self):
        self.ip.updatepersist(current = "1.1.1.1")
    
    def test_getpreviousip(self):
        self.assertEqual(self.ip.getpreviousip(), "1.1.1.1")

    def test_getconfig(self):
        self.assertIsInstance(main.getconfig(), list)

    def test_gettoken(self):
        self.assertNotEqual(main.gettoken(), None)