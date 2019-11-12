import configparser
import os

CONFIG_FILE = 'config.ini'
server_config = configparser.ConfigParser()

# a good way to fetch files
server_config.read(
    os.path.join(os.path.split(os.path.realpath(__file__))[0], CONFIG_FILE))
