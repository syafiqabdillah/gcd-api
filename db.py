import os
import psycopg2
import datetime
from dotenv import load_dotenv
import json
import uuid

load_dotenv()

DB_HOST=os.getenv('DB_HOST')
DB_NAME=os.getenv('DB_NAME')
DB_USER=os.getenv('DB_USER')
DB_PASS=os.getenv('DB_PASS')

def execute_get(query):
    connection = psycopg2.connect(
        user=DB_USER,
        host=DB_HOST,
        database=DB_NAME,
        password=DB_PASS,
    )
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def execute_post(query, val):
    try:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            database=DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(query, val)
        connection.commit()
        cursor.close()
        connection.close()
        return 'success'
    except:
        return 'failed'

def get_locations():
    query = """
            select location.name, sublocation.name, sublocation.is_crowded
            from location join sublocation
            on location.id = sublocation.id_location
            """
    lst = execute_get(query)
    result = {} # list of dict of sublocation
    for item in lst:
        if item[0] not in result.keys():
            result[item[0]] = [{
                'sublocation_name': item[1],
                'is_crowded': item[2]
            }]
        else:
            result[item[0]].append({
                'sublocation_name': item[1],
                'is_crowded': item[2]
            })

    return result
