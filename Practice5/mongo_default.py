from pymongo import MongoClient


def connect_mongo():
    client = MongoClient()
    db = client['test-db']
    return db.person


def insert_many(collection, data):
    collection.insert_many(data)
