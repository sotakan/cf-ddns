import unittest
import main

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