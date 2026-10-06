import psycopg2
from pymongo import MongoClient


def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="financial_risk_db",
        user="postgres",
        password="14316",
        port="5432"
    )


def get_mongo():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["financial_risk_db"]
    return db["risk_analysis"]