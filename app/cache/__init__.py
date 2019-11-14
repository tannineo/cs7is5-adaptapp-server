from redis import Redis

from config import server_config

# redis settings
db = server_config.get('redis', 'db')
host = server_config.get('redis', 'host')
port = server_config.get('redis', 'port')

print('Connecting redis server ' + host + ':' + port + ' using db:' + db)

r = Redis(host, port, db)
