from unittest import TestCase
from utils.Config import ConfigSecurity


class TestSign(TestCase):
    def setUp(self):
        self.sec_config = ConfigSecurity()

    def test_get_public_key_path(self):
        self.assertEqual('../instance_test/public_key.pem', self.sec_config.public_key_path)
