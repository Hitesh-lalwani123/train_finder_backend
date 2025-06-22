from pymongo import MongoClient
import os
# Replace with your MongoDB Atlas connection string
from dotenv import load_dotenv
load_dotenv()
db_name = os.getenv("DB")
collection_name = os.getenv("COLLECTION")
username = os.getenv("MONGO_USER")
password = os.getenv("MONGO_PWD")



def create_connection():
    client = MongoClient(f"mongodb+srv://{username}:{password}@cluster0.wsh3nhc.mongodb.net/?retryWrites=true&w=majority&appName=cluster0")
    # Select database and collection
    return client


def read_document(client,date):
    db = client['train_data']
    collection = db['train_data']
    query = {date: {"$exists": True}}
    result = collection.find_one(query)
    return result

def read_all(client):
    db = client['train_data']
    collection = db['train_data']
    result = collection.find()
    return result
def close_connection(client):
    client.close()
    return
