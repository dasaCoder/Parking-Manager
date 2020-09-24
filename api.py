import flask
import mysql.connector
from mysql.connector import Error
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

DB_HOST='localhost'
DB = 'parking'
DB_USER = 'dbuser'
DB_PASSWORD = '123'


@app.route('/', methods=['GET'])
def home():
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/blocks', methods=['GET'])
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
            return flask.jsonify(records)
            print("MySQL connection is closed")
    


app.run()
