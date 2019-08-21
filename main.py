from flask import Flask, jsonify
import mysql.connector
from mysql.connector import Error
app = Flask(__name__)


def to_dict(headers, data):
    response = []
    for row in data:
        tmp = {}
        for i in range(len(headers)):
            tmp[headers[i]] = row[i]
        response.append(tmp)
    return response


@app.route('/')
def hello():
    return 'Hello'


@app.route('/tasks/<int:project_id>')
def get_tasks(project_id):
    try:
        connection = mysql.connector.connect(host='213.32.19.136',
                                             database='visian',
                                             user='visian',
                                             password='visian')
        cursor = connection.cursor()
        cursor.execute("select * from TasksFull where projectid = " + str(int(project_id)))
        records = cursor.fetchall()
        return jsonify(to_dict(cursor.column_names, records))
    except Error as e:
        print("Error reading data from MySQL table", e)
        return jsonify([])
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    app.run()
