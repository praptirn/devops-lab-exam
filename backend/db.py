import os
from pymongo import MongoClient

# MongoDB Atlas connection placeholder
# In a real app, use environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://praptinayak2005_db_user:kaBeeRaa@cluster1.aunpexn.mongodb.net/?appName=Cluster1")
client = MongoClient(MONGO_URI)
db = client['taskflow']
