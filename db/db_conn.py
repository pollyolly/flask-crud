import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "v68qwiX7Ft!d",
    "database": "flask_crud"
}

def get_db_connection():
    return mysql.connector.connect(**db_config)