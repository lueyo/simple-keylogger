from pymongo import MongoClient

# config.py

class Config:
    client = "mongodb://localhost:27017/"
    db = "keylogger"
    collection = "keys"
    
