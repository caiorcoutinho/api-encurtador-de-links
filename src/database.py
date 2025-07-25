import mysql.connector
from datetime import datetime
import os
from mysql.connector.errors import IntegrityError

ALL_USERS_ID = 0

def get_connection():
    return mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE"),
    port=os.getenv('DB_PORT'),
)



def create(original_url, shorten_url, user=ALL_USERS_ID,):

    already_exists = find_original_url(shorten_url)

    if already_exists:
        return False

    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        connection = get_connection()
        cursor = connection.cursor()
        query='INSERT INTO links (original_url, shorten_url, user, date) VALUES (%s, %s, %s, %s);'
        cursor.execute(query, (original_url, shorten_url, user, date,))
        connection.commit()
        return True
    except IntegrityError:
        return False
    finally:
        connection.close()

def find_original_url(shorten_url):
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = 'SELECT * FROM links WHERE shorten_url=%s;'
        cursor.execute(query, (shorten_url,))
        result = cursor.fetchone()
        if not result:
            return None
        data = {"original_url": result[0]}
        return data
    finally:
        connection.close()
