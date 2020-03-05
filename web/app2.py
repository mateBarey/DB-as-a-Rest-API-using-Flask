'''
Registration of a user
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrieve his stored sentence on our database for 1 token
'''
from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.SentencesDatabase
users = db['Users']

class Register(Resource):
    def post(self):
        #step 1 to get posted data by the users
        postedData = request.get_json()

        #get the database
        username = postedData['username']
        password = postedData['password'] #'123xyz'

        #hash(password + salt) = adfaksfjksnfasf
        hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        #store username and paw into the db
        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Sentence": "",
            "Tokens":6
        })

        retJson = {
            "status":200,
            "msg": "You sucessfuly signed up for the API",
        }
        return jsonify(retJson)

def verifyPw(username, password):
    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def countTokens(username):
    tokens = users.find({
        "Username":username
    })[0]["Tokens"]
    return tokens


class Store(Resource):
    def post(self):
        #step 1 get posted data
        postedData = request.get_json()

        #step 2 read the data
        username = postedData['username']
        password = postedData['password']
        sentence = postedData['sentence']

        #step 3 verify the username pw match
        correct_pw = verifyPw(username, password)

        if not correct_pw:
            retJson = {
                'status':302
            }
            return jsonify(retJson)
        #step 4 verify user has enough tokens
        num_tokens = countTokens(username)
        if num_tokens <= 0:
            retJson ={
                "status": 301
            }
            return jsonify(retJson)
        #step 5 store sentence and return 200 ok
        users.update({
            "Username":username
        }, {
            "$set":{
                "Sentence":sentence,
                "Tokens":num_tokens-1
                }
        })
        retJson = {
            "status":200,
            "msg":"Sentence saved successfully"
        }
        return jsonify(retJson)

class Get(Resource):
    def post(self):
            postedData = request.get_json()
            username = postedData['username']
            password = postedData['password']

            correct_pw = verifyPw(username, password)

            if not correct_pw:
                retJson = {
                    'status':302
                }
                return jsonify(retJson)

            num_tokens = countTokens(username)
            if num_tokens <= 0:
                retJson ={
                    "status": 301
                }
                return jsonify(retJson)

            #make user pay!
            users.update({
                "Username":username
            }, {
                "$set":{
                    "Tokens":num_tokens-1
                    }
            })

            sentence = users.find({
                "Username": username
            })[0]["Sentence"]

            retJson = {
                "status":200,
                "sentence": sentence

            }

            return jsonify(retJson)


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__=="__main__":
    app.run(host='0.0.0.0')
'''
from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient('mongodb://db:27017')
db = client.aNewDB
UserNum = db['UserNum']

UserNum.insert({
    'num_of_users':0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]['num_of_users']
        new_num = prev_num + 1
        UserNum.update({}, {"$set":{'num_of_users':new_num}})
        return str("Hello user " + str(new_num))

def checkPostedData(postedData, functionName):
    if (functionName == 'add' or functionName == 'subtract' or functionName == 'multiply'):
        if 'x' not in postedData or 'y' not in  postedData:
            return 301 #missing parameter
        else:
            return 200
    elif (functionName == 'division'):
        if 'x' not in postedData or 'y' not in  postedData:
            return 301 #missing parameter
        elif int(postedData['y'])==0:
            return 302
        else:
            return 200

class Add(Resource):
    def post(self):
        #If i am here, then the  resource add was requested using the method post

        #step 1 get posted data
        postedData = request.get_json()

        #step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, 'add')
        if (status_code!=200):
            retJson = {
                'Message': 'An error happened',
                'Status code':status_code
            }
            return jsonify(retJson)

        # If im here then status code = 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        #step 2 add posted data
        ret = x + y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)


class Subtract(Resource):
    def post(self):
        #If i am here, then the  resource subtract was requested using the method post

        #step 1 get posted data
        postedData = request.get_json()

        #step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, 'subtract')
        if (status_code!=200):
            retJson = {
                'Message': 'An error happened',
                'Status code':status_code
            }
            return jsonify(retJson)

        # If im here then status code = 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        #step 2 add posted data
        ret = x - y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Multiply(Resource):
    def post(self):
        #If i am here, then the  resource multiply was requested using the method post

        #step 1 get posted data
        postedData = request.get_json()

        #step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, 'multiply')
        if (status_code!=200):
            retJson = {
                'Message': 'An error happened',
                'Status code':status_code
            }
            return jsonify(retJson)

        # If im here then status code = 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        #step 2 multiply posted data
        ret = x * y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

class Divide(Resource):
    def post(self):
        #If i am here, then the  resource divide was requested using the method post

        #step 1 get posted data
        postedData = request.get_json()

        #step 1b: Verify validity of posted data
        status_code = checkPostedData(postedData, 'division')
        if (status_code!=200):
            retJson = {
                'Message': 'An error happened',
                'Status code':status_code
            }
            return jsonify(retJson)

        # If im here then status code = 200
        x = postedData['x']
        y = postedData['y']
        x = int(x)
        y = int(y)

        #step 2 multiply posted data
        ret = (x*1.0)/ y
        retMap = {
            'Message': ret,
            'Status Code': 200
        }
        return jsonify(retMap)

api.add_resource(Add, '/add')
api.add_resource(Subtract, '/subtract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/division')
api.add_resource(Visit, '/hello')


@app.route('/')

def hello_world():
    return "Hello World!"

if __name__=="__main__":
    app.run(host='0.0.0.0')
'''
