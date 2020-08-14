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

## query must include RETURNING ID in the end 
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
        returning_id = cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return {
            'message': 'success',
            'data': {
                'returning_id': returning_id
            }
        }
    except Exception as e:
        print(str(e))
        return {
            'message': 'failed'
        }

def add_location(name):
    query = "insert into location(name) values (%s) returning id"
    value = (name, )
    return execute_post(query, value)

def add_sublocation(id_location, name):
    query = "insert into sublocation(id_location, name) values (%s, %s) returning id"
    value = (id_location, name)
    return execute_post(query, value)

def add_crowd_data(sublocation_id, is_crowded, created_at):
    query = "insert into crowd_density(sublocation_id, is_crowded,created_at) values (%s, %s, %s) returning id"
    value = (sublocation_id, is_crowded, created_at)
    return execute_post(query, value)

def get_location_names():
    query = "select id, name, is_active from location"
    lst = execute_get(query)
    result = []
    for item in lst:
        result.append({
            'id': item[0],
            'name': item[1],
            'is_active': item[2]
        })
    return result

def get_locations():
    query = """
            select location.id, location.name, sublocation.name, crowd_density.is_crowded, crowd_density.created_at
            from (location join sublocation
            on location.id = sublocation.id_location) join crowd_density
            on sublocation.id = crowd_density.sublocation_id
            """
    lst = execute_get(query)
    result = {} # list of dict of sublocation
    for item in lst:
        if item[1] not in result.keys(): # belum ada 
            result[item[1]] = {}
            result[item[1]]['id'] = item[0]
            result[item[1]]['sublocations'] = [{
                'sublocation_name': item[2],
                'is_crowded': item[3],
                'created_at': item[4],
            }]
        else:
            result[item[1]]['sublocations'].append({
                'sublocation_name': item[2],
                'is_crowded': item[3],
                'created_at': item[4],
            })

    return result
