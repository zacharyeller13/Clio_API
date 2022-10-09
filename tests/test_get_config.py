from configparser import ConfigParser
import os
from get_authorization import Config

curpath = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(curpath, "test_config.ini")
config = Config(file)

def test_config():
    assert isinstance(config, ConfigParser) == True

def test_get_client_id():
    assert config.client_id == "test_client_id"

def test_get_client_secret():
    assert config.client_secret == "test_client_secret"
