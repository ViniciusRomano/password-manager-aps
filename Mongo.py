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

    def get_all_websites(self, user):
        data = self.users.find({"user": user["user"]}, {"web_data"})
        return data

    def get_website(self, user, website):
        data = self.users.find_one({"user": user["user"]}, {"web_data": {
                                   "$elemMatch": {"website": website}}})
        return data

    def update_password(self, user):
        self.user = user
        self.users.update_one({'_id': user['_id']}, {
                              "$set": {"password": user["password"]}})

    def insert_website(self, user):
        self.user = user
        self.users.update_one({'_id': user['_id']}, {
                              "$set": {"web_data": user["web_data"]}})

    def remove_website(self, user, website):
        self.user = user
        self.users.update_one({'_id': user['_id']}, {
                              "$pull": {"web_data": {"website": website}}})
