# File: db.py
from pymongo import MongoClient

# Connect to local MongoDB instance
db_client = MongoClient("mongodb://localhost:27017")
# Use database 'certificate_db' and collection 'users'
db = db_client["certificate_db"]
users_collection = db["users"]