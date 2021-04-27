from flask import Flask, request
from flask_restful import Resource, Api
from json import dumps
import json
import uuid

app = Flask(__name__)
api = Api(app)
houseKey = {}
userKey = {}
houseDict = {}
roomLightStatus = {}
doorLockStatus = {}
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
            if roomLightStatus[roomName]:
                roomStatus = "off"
            else:
                roomStatus = "on"

            roomLightStatus[roomName] = not roomLightStatus[roomName]

        if userID in userKey:
            userName = userKey[userID]
        print(roomName)
        print(userName)
        if roomName == "" or userName == "":
            return {"code": 400, "message": "Room ID or user ID not valid"}

        print("Light was turned {} in {} by {}".format(roomStatus, roomName, userName))
        return {"code": 200, "message": "Light was turned {} in {} by {}".format(roomStatus, roomName, userName)}

class DoorLock(Resource):
    
    # lock/unlock door
    def get(self):
        args = request.args
        userID = args['userID']
        roomID = args['roomID']
        roomName = ""
        userName = ""
        
        if roomID in houseKey:
            roomName = houseKey[roomID]
            if doorLockStatus[roomName]:
                roomStatus = "unlocked"
            else:
                roomStatus = "locked"

            doorLockStatus[roomName] = not doorLockStatus[roomName]

        if userID in userKey:
            userName = userKey[userID]

        if roomName == "" or userName == "":
            return {"code": 200, "message": "Room ID or user ID not valid"}

        print("Light was turned {} in {} by {}".format(roomStatus, roomName, userName))
        return {"code": 200, "message": "{} was {} by {}".format(roomName, roomStatus, userName)}

class CreateUser(Resource):
    def get(self):
        args = request.args
        newUserID = str(uuid.uuid4())
        newUserName = args['userName']

        if newUserName in userKey.values():
            print("User already exists!")
            return {"code": 400, "message": "user already exists"}

        userKey[newUserID] = newUserName
        saveDatabase()

        print("New user added! Username: {} User ID: {}".format(newUserName, newUserID))
        
        return {"code": 200, "message": "new user successfully added", "user": {"name": newUserName, "id": newUserID}}

class DeleteUser(Resource):
    def get(self):
        args = request.args
        userID = args['userID']
        
        if userID in userKey:
            del userKey[userID]
            saveDatabase()
            return {"code": 200, "message": "successfully deleted user"}
        
        return {"code": 400, "message": "failed to delete user"}

class VerifyUser(Resource):
    def get(self):
        args = request.args
        userID = args['userID']

        if userID in userKey:
            
            # user already exists
            print("User already exists! User ID: {}".format(userID))
            return {"code": 200, "message": "user already exists"}

        print("User does not exist! User ID: {}".format(userID))
        return {"code": 400, "message": "user does not exist"}

class Main(Resource):
    def get(self):
        print("House Simulator is running!")
        return {"code": 200, "message": "house simulator is running"}

def saveDatabase():
    with open('db.json', 'w') as f:
        entire_db = {"house status": {"door lock status": doorLockStatus, "room light status": roomLightStatus}, "house key": houseKey, "user key": userKey}
        json.dump(entire_db, f)

def loadDatabase():
    global houseDict, houseKey, userKey, roomLightStatus, doorLockStatus
    f = open('db.json')
    raw_data = json.load(f)
    houseDict = raw_data['house status']
    roomLightStatus = raw_data['house status']['room light status']
    doorLockStatus = raw_data['house status']['door lock status']
    userKey = raw_data['user key']
    houseKey = raw_data['house key']
    print(houseDict)
    print(roomLightStatus)
    print(doorLockStatus)
    print(userKey)
    print(houseKey)

# api route definitions
api.add_resource(Light, '/Lights/')
api.add_resource(CreateUser, '/CreateUser/')
api.add_resource(DeleteUser, '/DeleteUser/')
api.add_resource(VerifyUser, '/VerifyUser/')
api.add_resource(DoorLock, '/DoorLock/')
api.add_resource(Main, '/')

if __name__ == '__main__':
    try:
        loadDatabase()
        app.run(port='5002')
    except KeyboardInterrupt:
        pass
    finally:
        saveDatabase()