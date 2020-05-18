from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
@app.route('/hello')
def hello_world():
    return 'hello'

class Add(Resource):
    def get(self):
        return 'hello', 200

api.add_resource(Add, '/hello2')
