import os
from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.server_api import ServerApi

def get_uri(username: str, password: str, cluster_domain: str) -> str:
    return f"mongodb+srv://{username}:{password}@{cluster_domain}/?retryWrites=true&w=majority"

def get_uri_cripto_db() -> str:
    username = os.getenv('MONGO_CRIPTO_USER')
    password = os.getenv('MONGO_CRIPTO_PASSWORD')
    cluster_domain = os.getenv("MONGO_CRIPTO_CLUSTER_DOMAIN")
    return get_uri(username, password, cluster_domain)

def get_client_cripto_db() -> MongoClient:
    uri = get_uri_cripto_db()
    client = MongoClient(uri, server_api = ServerApi('1'))
    return client

def get_klines_cripto_db(client: MongoClient) -> Database:
    return client[os.getenv('MONGO_CRIPTO_KLINES')]