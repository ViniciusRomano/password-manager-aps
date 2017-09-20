from pymongo import MongoClient


class Mongo:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        db = client.passmanager
        self.users = db.users

    def insert_user(self, data):
        self.data = data
        self.users.insert_one(data)

    def get_user(self, user):
        data = self.users.find_one({"user": user})
        return data
