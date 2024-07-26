#connect to local mongo
from pymongo import MongoClient
from config import Config

client = MongoClient(Config.client)
db = client[Config.db]
keys_collection = db[Config.collection]