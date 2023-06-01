
import os
import pymysql
from flask import jsonify
import json

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format('oecs1-cc-06:us-central1:patient-info-001')
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user='namrata', password='namrata',
                                unix_socket=unix_socket, db='patients',
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn



def get_info():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM info;')
        info = cursor.fetchall()
        if result > 0:
            # Convert the results to a list of dictionaries
            info_list = []
            for row in info:
                row_dict = {
                    'id': row[0],
                    'name': row[1],
                    'gender': row[2],
                    'age': row[3],
                    'address': row[4],
                    'number': row[5],
                    'diagnosis': row[6],
                    'doctor': row[7]
                }
                info_list.append(row_dict)
                
            got_info = json.loads(json.dumps(info_list))
        else:
            got_info = 'No info in DB'
    conn.close()
    return got_info

def add_info(info):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO info (name ,gender,age,address,number,diagnosis,doctor) VALUES(%s,%s,%s,%s,%s,%s,%s)', (info["name"], info["gender"], info["age"],info["address"],info["number"],info["diagnosis"],info["doctor"]))
    conn.commit()
    conn.close()

def update_info(patient_id, new_info):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('UPDATE info SET name=%s, gender=%s, age=%s, address=%s, number=%s, diagnosis=%s, doctor=%s WHERE PatientID=%s', (new_info["name"], new_info["gender"], new_info["age"], new_info["address"], new_info["number"], new_info["diagnosis"], new_info["doctor"], patient_id))
    conn.commit()
    conn.close()

def delete_info(patient_id):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM info WHERE PatientID=%s', (patient_id,))
    conn.commit()
    conn.close()
