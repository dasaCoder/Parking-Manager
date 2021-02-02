import flask
import mysql.connector
from mysql.connector import Error
import json
from flask import request, jsonify
from flask_cors import CORS, cross_origin

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app)

DB_HOST='localhost'
DB = 'parking'
DB_USER = 'dbuser'
DB_PASSWORD = '123'


@app.route('/', methods=['GET'])
@cross_origin()
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/blocks', methods=['GET'])
@cross_origin()
def getBlock():
    records = []

    try:
        connection = mysql.connector.connect(host=DB_HOST,
                                            database=DB,
                                            user=DB_USER,
                                            password=DB_PASSWORD)
        sql_select_Query = "select id,name,state,type from slots"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in Laptop is: ", cursor.rowcount)
        print("\nPrinting each laptop record")
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            response = flask.jsonify(records)
            return response
            print("MySQL connection is closed")


#states -> 0 unavailable 1 available 2 booked
@app.route('/blocks', methods=['POST'])
@cross_origin()
def addBlock():
    print(request.json)
    records = []

    try:
        connection = mysql.connector.connect(host=DB_HOST,
                                            database=DB,
                                            user=DB_USER,
                                            password=DB_PASSWORD)
        sql_select_Query = "insert into slots(name,state,type, slot) values('"+ request.json['name'] + "'," +request.json['state'] +",'" + request.json['type']+"', '"+ request.json['slot'] +"')"
        cursor = connection.cursor()  
        cursor.execute(sql_select_Query)
    except Error as e:
        print("Error saving data to MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            return flask.jsonify(records)
            print("MySQL connection is closed")

@app.route('/slot/book', methods=['POST'])
@cross_origin()
def bookSlot():
        try:
            connection = mysql.connector.connect(host=DB_HOST,
                                                database=DB,
                                                user=DB_USER,
                                                password=DB_PASSWORD)
            sql_select_Query = "INSERT INTO `parking`.`bookings` (`slot_id`, `date`, `vehicle_no`) VALUES ('"+ str(request.json['slot_id']) +"', '"+request.json['date']+"', '"+request.json['vehicle_no']+"')"
            print(sql_select_Query)
            cursor = connection.cursor()  
            cursor.execute(sql_select_Query)
            connection.commit()
        except Error as e:
            print("Error saving data to MySQL table", e)
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
                return {"success":True}


@app.route('/slot/rent', methods=['POST'])
@cross_origin()
def rentSlot():
        try:
            connection = mysql.connector.connect(host=DB_HOST,
                                                database=DB,
                                                user=DB_USER,
                                                password=DB_PASSWORD)
            sql_select_Query = "INSERT INTO `parking`.`parking_log` (`vehicle_no`, `check_in`, `slot_id`, `date`) VALUES ('"+request.json['vehicle_no']+"', '"+request.json['check_in']+"', '"+ str(request.json['slot_id']) +"', '"+request.json['date']+"');"
            # make slot unavailable
            update_query = "UPDATE `parking`.`slots` SET `state` = '0' WHERE (`id` = '"+ str(request.json['slot_id']) +"');"
            print(sql_select_Query)
            cursor = connection.cursor()  
            cursor.execute(sql_select_Query)
            cursor.execute(update_query)
            connection.commit()
        except Error as e:
            print("Error saving data to MySQL table", e)
            return {"success":False} 
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
                return {"success":True}

@app.route('/slot/rent/end', methods=['POST'])
@cross_origin()
def endRentSlot():
        try:
            connection = mysql.connector.connect(host=DB_HOST,
                                                database=DB,
                                                user=DB_USER,
                                                password=DB_PASSWORD)
            update_query = "UPDATE `parking`.`parking_log` SET `check_out` = '"+request.json['check_out']+"' WHERE (`slot_id` = '"+ str(request.json['slot_id']) +"' and `check_out` IS NUll);"
            print(update_query)
            state_update_query = "UPDATE `parking`.`slots` SET `state` = '1' WHERE (`id` = '"+ str(request.json['slot_id']) +"');"

            cursor = connection.cursor()  
            cursor.execute(update_query)
            cursor.execute(state_update_query)
            connection.commit()
        except Error as e:
            print("Error saving data to MySQL table", e)
            return {"success":False} 
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")
                return {"success":True}               

app.run()
