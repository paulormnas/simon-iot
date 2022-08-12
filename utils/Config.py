import configparser
from dotenv import load_dotenv

from os import path, environ


class Config(object):
    def __init__(self):
        mode = (
            environ["SIMON_IOT_MODE"] if "SIMON_IOT_MODE" in environ else "development"
        )
        config_path = path.join(
            path.abspath(path.dirname(__file__)), f"../instance_{mode}/config.cfg"
        )
        env_path = path.join(
            path.abspath(path.dirname(__file__)), f"../calibration.env"
        )
        load_dotenv(env_path)
        self.config = configparser.ConfigParser()
        self.config.read(config_path)

    def get_property(self, section, property_name):
        property_value = None
        if section in self.config and property_name in self.config[section]:
            property_value = self.config[section][property_name]
        return property_value


class ConfigSecurity(Config):
    def __init__(self):
        super().__init__()

    @property
    def public_key_path(self):
        return self.get_property(section="security", property_name="public_key")

    @property
    def private_key_path(self):
        return self.get_property(section="security", property_name="private_key")


class ConfigDeviceInfo(Config):
    def __init__(self):
        super().__init__()

    @property
    def id(self):
        return self.get_property(section="device", property_name="id")

    @property
    def location(self):
        return self.get_property(section="device", property_name="location")

    @property
    def type(self):
        return self.get_property(section="device", property_name="type")


class ConfigServer(Config):
    def __init__(self):
        super().__init__()

    @property
    def url(self):
        return self.get_property(section="server", property_name="url")

    @property
    def port(self):
        return self.get_property(section="server", property_name="port")


class ConfigSensors(Config):
    def __init__(self):
        super().__init__()

    @property
    def DHT_pin(self):
        return int(self.get_property(section="DHT", property_name="pin"))

    @property
    def DHT_number_of_readings(self):
        return int(self.get_property(section="DHT", property_name="number_of_readings"))

    @property
    def DHT_interval(self):
        return int(self.get_property(section="DHT", property_name="interval"))

    @property
    def PIR_pin(self):
        return int(self.get_property(section="PIR", property_name="pin"))

    @property
    def PIR_interval(self):
        return int(self.get_property(section="PIR", property_name="interval"))
