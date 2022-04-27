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

class TestMainCloudflare(unittest.TestCase):
    def test_init(self):
        main.cloudflare()

    @classmethod
    def setUp(self) -> None:
        self.cf = main.cloudflare()

    def test_gettoken(self):
        self.assertNotEqual(self.cf.token, None)

    def test_getconfig(self):
        self.assertIsInstance(self.cf.config, list)

    def test_getzoneid(self):
        self.assertEqual(self.cf.getzoneid(os.getenv("CFDDNS_TEST_DOMAIN")), os.getenv("CFDDNS_TEST_ZONEID"))

    def test_getrecord(self):
        zoneid = self.cf.getzoneid(os.getenv("CFDDNS_TEST_DOMAIN"))
        self.assertEqual(self.cf.getrecord(zoneid, os.getenv("CFDDNS_TEST_SUBDOMAIN")), (os.getenv("CFDDNS_TEST_TESTRECORD"), "A"))

    def test_updaterecord(self):
        zoneid = self.cf.getzoneid(os.getenv("CFDDNS_TEST_DOMAIN"))
        record = self.cf.getrecord(zoneid, os.getenv("CFDDNS_TEST_SUBDOMAIN"))

        # Check if record is A
        if record[1] != "A":
            raise Exception("Test record is not A")


        self.assertTrue(self.cf.updaterecord(zoneid, record[3], os.getenv("CFDDNS_TEST_SUBDOMAIN"), "192.168.245.1", record[2]))

        self.cf.updaterecord(zoneid, record[3], os.getenv("CFDDNS_TEST_SUBDOMAIN"), os.getenv("CFDDNS_TEST_TESTRECORD"), record[2])