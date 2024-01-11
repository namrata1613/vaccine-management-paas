
import os
import pymysql
from flask import jsonify
import json

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')


def open_connection():
    unix_socket = '/cloudsql/{}'.format('oecs1-cc-06:us-central1:vaccine-mangement-info-001')
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user='USER', password='PASSWORD',
                                unix_socket=unix_socket, db='vaccine-management',
                                cursorclass=pymysql.cursors.DictCursor
                                )
    except pymysql.MySQLError as e:
        print(e)

    return conn


def insert_diagnosed(info):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO Diagnosed (RTPCRId,EpId,LeavingDate,Hospital) VALUES(%s,%s,%s,%s)', (info["RTPCRId"], info["EpId"], info["LeavingDate"],info["Hospital"]))
    conn.commit()
    conn.close()



def insert_regularCheckup(info):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO RegCheckup (EpId,Result) VALUES(%s,%s)', (info["EpId"], info["Result"]))
    conn.commit()
    conn.close()

def insert_vaccination(info):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO vaccination (CertNo,vaccineName,Id,FirstVaccineDate,SecondVaccineDate) VALUES(%s,%s,%s,%s,%s)', (info["CertNo"], info["vaccineName"],info["Id"],info["FirstVaccineDate"],info["SecondVaccineDate"]))
    conn.commit()
    conn.close()


def get_info():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM (select * from vaccination join employee on Id=EpId) union (select * vaccination join student on Id=SId);')
        info = cursor.fetchall()
        if result > 0:
            # Convert the results to a list of dictionaries
            info_list = []
            for row in info:
                row_dict = {
                    'Name': row[0],
                    'CertNo': row[1],
                    'vaccineName': row[2],
                    'Id': row[3],
                    'FirstVaccineDate': row[4],
                    'SecondVaccineDate': row[5]
                }
                info_list.append(row_dict)
                
            got_info = json.loads(json.dumps(info_list))
        else:
            got_info = 'No info in DB'
    conn.close()
    return got_info

def get_upcomingDoseInfo():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM upcoming_dose;')
        info = cursor.fetchall()
        if result > 0:
            # Convert the results to a list of dictionaries
            info_list = []
            for row in info:
                row_dict = {
                    'SId': row[0],
                    'Sname': row[1],
                    'Second_Dose_dates': row[2]
                }
                info_list.append(row_dict)
                
            got_info = json.loads(json.dumps(info_list))
        else:
            got_info = 'No info in DB'
    conn.close()
    return got_info


def get_diagnosedInfo():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM Diagnosed;')
        info = cursor.fetchall()
        if result > 0:
            # Convert the results to a list of dictionaries
            info_list = []
            for row in info:
                row_dict = {
                    'RTPCRId': row[0],
                    'EpId': row[1],
                    'LeavingDate': row[2],
                    'Hospital': row[3],
                    'quarantine_days': row[4],
                }
                info_list.append(row_dict)
                
            got_info = json.loads(json.dumps(info_list))
        else:
            got_info = 'No info in DB'
    conn.close()
    return got_info



# def get_info():
#     conn = open_connection()
#     with conn.cursor() as cursor:
#         result = cursor.execute('SELECT * FROM info;')
#         info = cursor.fetchall()
#         if result > 0:
#             # Convert the results to a list of dictionaries
#             info_list = []
#             for row in info:
#                 row_dict = {
#                     'id': row[0],
#                     'name': row[1],
#                     'gender': row[2],
#                     'age': row[3],
#                     'address': row[4],
#                     'number': row[5],
#                     'diagnosis': row[6],
#                     'doctor': row[7]
#                 }
#                 info_list.append(row_dict)
                
#             got_info = json.loads(json.dumps(info_list))
#         else:
#             got_info = 'No info in DB'
#     conn.close()
#     return got_info

# def add_info(info):
#     conn = open_connection()
#     with conn.cursor() as cursor:
#         cursor.execute('INSERT INTO info (name ,gender,age,address,number,diagnosis,doctor) VALUES(%s,%s,%s,%s,%s,%s,%s)', (info["name"], info["gender"], info["age"],info["address"],info["number"],info["diagnosis"],info["doctor"]))
#     conn.commit()
#     conn.close()

# def update_info(patient_id, new_info):
#     conn = open_connection()
#     with conn.cursor() as cursor:
#         cursor.execute('UPDATE info SET name=%s, gender=%s, age=%s, address=%s, number=%s, diagnosis=%s, doctor=%s WHERE PatientID=%s', (new_info["name"], new_info["gender"], new_info["age"], new_info["address"], new_info["number"], new_info["diagnosis"], new_info["doctor"], patient_id))
#     conn.commit()
#     conn.close()

# def delete_info(patient_id):
#     conn = open_connection()
#     with conn.cursor() as cursor:
#         cursor.execute('DELETE FROM info WHERE PatientID=%s', (patient_id,))
#     conn.commit()
#     conn.close()
