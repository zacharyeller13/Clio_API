from configparser import ConfigParser
import os
from ..Clio_API_GetAuthorization import get_config, get_client_id, get_client_secret

curpath = os.path.dirname(os.path.realpath(__file__))
file = os.path.join(curpath, "test_config.ini")

def test_get_config():
    assert isinstance(get_config(file), ConfigParser) == True

def test_get_client_id():
    config = get_config(file)
    assert get_client_id(config) == "test_client_id"

def test_get_client_secret():
    config = get_config(file)
    assert get_client_secret(config) == "test_client_secret"