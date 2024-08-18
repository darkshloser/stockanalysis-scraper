import os
import configparser

def get_config():
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '../config.ini')
    config.read(config_path)
    return config

def get_settings():
    config = get_config()
    return config['settings']

