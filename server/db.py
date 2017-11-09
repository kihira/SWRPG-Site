import os
from pymongo import MongoClient

client = MongoClient(os.environ['DB_CONN'])
db = client.starwars
