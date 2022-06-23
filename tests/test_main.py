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
        res = self.cf.getrecord(zoneid, os.getenv("CFDDNS_TEST_SUBDOMAIN"))
        self.assertEqual(res["content"], os.getenv("CFDDNS_TEST_TESTRECORD"))
        self.assertEqual(res["type"], "A")

    def test_updaterecord(self):
        zoneid = self.cf.getzoneid(os.getenv("CFDDNS_TEST_DOMAIN"))
        test_record = self.cf.getrecord(zoneid, os.getenv("CFDDNS_TEST_SUBDOMAIN"))
        self.cf.updaterecord(zoneid, test_record["record_id"], os.getenv("CFDDNS_TEST_SUBDOMAIN"), "0.0.0.0", test_record["proxy"])
        
        # Test if things are in order...
        res = self.cf.getrecord(zoneid, os.getenv("CFDDNS_TEST_SUBDOMAIN"))
        self.assertEqual(res["content"], "0.0.0.0")
        self.assertEqual(res["type"], "A")
        self.assertEqual(res["proxy"], test_record["proxy"])

        # Revert changes
        self.cf.updaterecord(zoneid, test_record["record_id"], os.getenv("CFDDNS_TEST_SUBDOMAIN"), os.getenv("CFDDNS_TEST_TESTRECORD"), test_record["proxy"])

