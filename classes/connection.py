import mysql.connector

def connexion():
    return mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="temporaire"
)