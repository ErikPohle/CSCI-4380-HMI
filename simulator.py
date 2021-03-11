from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import json

app = Flask(__name__)
api = Api(app)
houseKey = {"1": 'living room', "2": 'dining room', "3": 'kitchen', "4": 'garage', "5": 'bathroom', "6": 'bedroom'}
userKey = {"1": "Erik", "2": "Jackson"}
class Light(Resource):
    
    def get(self):
        f = open('db.json')
        houseDict = json.load(f)
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

        with open('db.json', 'w') as f:
            json.dump(houseDict, f)
        print("Light was turned {} in {} by {}".format(roomStatus, roomName, userName))
        return "Light was turned {} in {} by {}".format(roomStatus, roomName, userName)
        

api.add_resource(Light, '/')

if __name__ == '__main__':
     app.run(port='5002')