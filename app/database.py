from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

connection_url = os.getenv("MONGODB_CONN_URI")

class DBClient:
    _client = None

    @staticmethod
    def get_client():
        if DBClient._client is None:
            try:
                DBClient._client = MongoClient(connection_url)
            except Exception as e:
                print("Error connecting to MongoDB: ", e);
                exit(1)
        return DBClient._client

    @staticmethod
    def get_db(db_name):
        if DBClient._client is None:
            print("DB doesn't have a client yet, try calling get_client() first!")
            return None
        return DBClient.get_client()[db_name]
