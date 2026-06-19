from pymongo import MongoClient
import pymongo

def get_database():

    client = MongoClient("mongodb://localhost:27017")

    return client['monitor_sensors']