from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
from passlib.context import CryptContext


app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentenceDatabase
users = db['Users']

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

class Ping(Resource):
    def get(self):
        return jsonify("pong")

class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        
        hashed_pw = pwd_context.hash(password)

        users.insert({
            'Username': username,
            'Password': hashed_pw,
            'Sentence': '',
            'Tokens': 6 
            })

        ret_json = {
                'status' : 200,
                'msg': 'Success'
                }
        return jsonify(ret_json)

def verify_pw(username, password):
    hashed_pw = users.find({
        "Username": username
        })[0]["Password"]
    if pwd_context.verify(password, hashed_pw):
        return True
    else:
        return False

def count_tokens(username):
    tokens = users.find({
        "Username": username
        })[0]["Tokens"]
    return tokens


class Store(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        sentence = posted_data['sentence']
        
        correct_pw = verify_pw(username, password)
        if not correct_pw:
            ret_json = {
                    'status': 302
                    }
            return jsonify(ret_json)

        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            ret_json = {
                    'status': 301
                    }
            return jsonify(ret_json)

        users.update({
            'Username': username,
        },{
            '$set':{
                    'Sentence':sentence,
                    'Tokens': num_tokens -1
                    }

        })
        
        ret_json = {
                'status': 200,
                'msg': 'saved'
                }
        return jsonify(ret_json)

class Get(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data['username']
        password = posted_data['password']
        
        correct_pw = verify_pw(username, password)
        if not correct_pw:
            ret_json = {
                    'status': 302
                    }
            return jsonify(ret_json)

        num_tokens = count_tokens(username)
        if num_tokens <= 0:
            ret_json = {
                    'status': 301
                    }
            return jsonify(ret_json)

        sentence = users.find({
            'Username': username
            })[0]['Sentence']

        ret_json = {
                'status': 200,
                'sentence': sentence
                }
        return jsonify(ret_json)



api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')
api.add_resource(Ping, '/ping')

if __name__ == '__main__':
    app.run(debug = True)
