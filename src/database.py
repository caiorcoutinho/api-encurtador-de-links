import mysql.connector
from datetime import datetime
import os
from mysql.connector.errors import IntegrityError

ALL_USERS_ID = 0

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_DATABASE"),
    port=os.getenv('DB_PORT'),
)



def create(original_url, shorten_url, user=ALL_USERS_ID,):
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor = connection.cursor()
    query='INSERT INTO links (original_url, shorten_url, user, date) VALUES (%s, %s, %s, %s);'
    try:
        cursor.execute(query, (original_url, shorten_url, user, date,))
    except IntegrityError:
        return False
    else:
        connection.commit()
        return True

def find_original_url(shorten_url):
    cursor = connection.cursor()
    query = 'SELECT * FROM links WHERE shorten_url=%s;'
    cursor.execute(query, (shorten_url,))
    result = cursor.fetchone()
    if not result:
        return None
    data = {"original_url": result[0]}
    return data
