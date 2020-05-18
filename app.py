from flask import Flask
from flask_restful import Api, Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentenceDatabase
users = db['Users']

class Hello(Resource):
    def get(self):
        return 'hello', 200

api.add_resource(Add, '/hello')
