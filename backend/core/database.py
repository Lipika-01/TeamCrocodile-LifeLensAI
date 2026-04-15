from pymongo import MongoClient
import os
from dotenv import load_dotenv
import sys

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "lifelens")

try:
    # Set serverSelectionTimeoutMS to 5000 to avoid long hangs on startup
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client[DATABASE_NAME]
    
    # Simple ping to verify connection
    client.admin.command('ping')
    
    # Collections
    users_collection = db.get_collection("users")
    records_collection = db.get_collection("health_records")
    
    print(f"Connected to MongoDB Atlas: {DATABASE_NAME}")
except Exception as e:
    print(f"DATABASE CONNECTION ERROR: {e}")
    print("WARNING: Platform running in offline mode. Records will not be saved.")
    # Initialize empty collections or mock them if needed
    users_collection = None
    records_collection = None
