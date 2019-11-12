from flask_mongoengine import MongoEngine
from config import server_config

db_name = server_config.get('mongo', 'db')
db_host = server_config.get('mongo', 'host')
db_port = server_config.get('mongo', 'port')

db = MongoEngine()
