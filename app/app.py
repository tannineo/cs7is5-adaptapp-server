from flask import Flask
from flask_restplus import Resource, Api

from model import db
from controller.user import user_api
from controller.pic import pic_api
from config import server_config

app = Flask(__name__)
# init db settings
app.config['MONGODB_SETTINGS'] = {
    'db': server_config.get('mongo', 'db'),
    'host': server_config.get('mongo', 'host'),
    'port': int(server_config.get('mongo', 'port'))
}
db.init_app(app)

server_api = Api(app, version='1.0.0', title='adapt-app', doc='/doc/')

# add namespaces (controllers) here
server_api.add_namespace(user_api)
server_api.add_namespace(pic_api)


@server_api.route('/hello')
class HelloSimple(Resource):
    def get(self):
        return {'hello': 'world'}


SERVER_HOST = server_config.get('server', 'host')
SERVER_PORT = server_config.get('server', 'port')

if __name__ == '__main__':
    app.run(debug=True, host=SERVER_HOST, port=SERVER_PORT)
