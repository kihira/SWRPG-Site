from pymongo import MongoClient
import os

client = MongoClient(os.environ['DB_CONN'])
db = client.starwars
