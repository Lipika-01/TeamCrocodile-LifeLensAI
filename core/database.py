from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "lifelens")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Collections
users_collection = db.get_collection("users")
records_collection = db.get_collection("health_records")

print(f"Connected to MongoDB: {DATABASE_NAME} database")
