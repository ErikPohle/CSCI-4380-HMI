from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import json
import signal
import sys

app = Flask(__name__)
api = Api(app)
houseKey = {}
userKey = {}
houseDict = {}
class Light(Resource):
    
    def get(self):
        args = request.args
        userID = args['userID']
        roomID = args['roomID']
        roomStatus = ""
        roomName = ""
        userName = ""
        
        if roomID in houseKey:
            roomName = houseKey[roomID]
            if houseDict[roomName]:
                roomStatus = "off"
            else:
                roomStatus = "on"

            houseDict[roomName] = not houseDict[roomName]

        if userID in userKey:
            userName = userKey[userID]

        if roomName == "" or userName == "":
            return "Room ID or user ID not valid"

        print("Light was turned {} in {} by {}".format(roomStatus, roomName, userName))
        return "Light was turned {} in {} by {}".format(roomStatus, roomName, userName)

class CreateUser(Resource):
    def get(self):
        args = request.args
        newUserID = args['userID']
        newUserName = args['userName']
        userKey[newUserID] = newUserName

        print("New user added! Username: {} User ID: {}".format(newUserName, newUserID))
        
        return 200

class VerifyUser(Resource):
    def get(self):
        args = request.args
        newUserID = args['userID']
        newUserName = args['userName']
        if userKey.get(newUserID):
            
            # user already exists
            print("User already exists! Username: {} User ID: {}".format(newUserName, newUserID))
            return 200

        print("User does not exist! Username: {} User ID: {}".format(newUserName, newUserID))
        return 400

class Main(Resource):
    def get(self):
        print("House Simulator is running!")
        return 200

def signal_handler(sig, frame):
    print('Shutting down simulator!')
    saveDatabase()
    sys.exit(0)

def saveDatabase():
    with open('db.json', 'w') as f:
        entire_db = {"house_status": {"room_light_status": houseDict}, "room_key": houseKey, "user_key": userKey}
        json.dump(entire_db, f)

def loadDatabase():
    global houseDict, houseKey, userKey
    f = open('db.json')
    raw_data = json.load(f)
    houseDict = raw_data['house_status']['room_light_status']
    userKey = raw_data['user_key']
    houseKey = raw_data['room_key']
    print(houseDict)
    print(userKey)
    print(houseKey)

# api route definitions
api.add_resource(Light, '/Lights/')
api.add_resource(CreateUser, '/CreateUser/')
api.add_resource(VerifyUser, '/VerifyUser/')
api.add_resource(Main, '/')

if __name__ == '__main__':
    loadDatabase()
    app.run(port='5002')