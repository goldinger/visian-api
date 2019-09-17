from flask import Flask, jsonify, request
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


@app.route('/projects/<int:project_id>')
def project(project_id):
    try:
        connection = mysql.connector.connect(host='213.32.19.136',
                                             database='visian',
                                             user='visian',
                                             password='visian')
        cursor = connection.cursor()
        cursor.execute("select * from TasksFull where projectid = " + str(int(project_id)))
        records = cursor.fetchall()
        records = to_dict(cursor.column_names, records)
        for record in records:
            cursor.execute("select * from Documents where tasktypeid = " + str(int(record.get('tasktypeid', 0))))
            documents = to_dict(cursor.column_names, cursor.fetchall())
            record['documents'] = documents
        response = jsonify(records)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Error as e:
        print("Error reading data from MySQL table", e)
        response = jsonify([])
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


@app.route('/entities/<int:entity_id>')
def entity(entity_id):
    try:
        connection = mysql.connector.connect(host='213.32.19.136',
                                             database='visian',
                                             user='visian',
                                             password='visian')
        cursor = connection.cursor()
        cursor.execute("select * from TasksFull where entityid = " + str(int(entity_id)))
        records = cursor.fetchall()
        records = to_dict(cursor.column_names, records)
        for record in records:
            cursor.execute("select * from Documents where tasktypeid = " + str(int(record.get('tasktypeid', 0))))
            documents = to_dict(cursor.column_names, cursor.fetchall())
            record['documents'] = documents
        response = jsonify(records)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Error as e:
        print("Error reading data from MySQL table", e)
        response = jsonify([])
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


@app.route('/tasks/<int:task_id>/setDone', methods=['GET', 'POST'])
def set_done(task_id):
    if request.method == 'POST':
        note = request.get_json(force=True).get('done')
        if note is None:
            response = jsonify({
                "status": "KO"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        try:
            connection = mysql.connector.connect(host='213.32.19.136',
                                                 database='visian',
                                                 user='visian',
                                                 password='visian')
            cursor = connection.cursor()
            cursor.execute("update Tasks set note = " + note + " where id = " + str(int(task_id)))
            connection.commit()
            response = jsonify({
                "status": "OK"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Error as e:
            print("Error updating data from MySQL table", e)
            response = jsonify({
                "status": "KO"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")


@app.route('/tasks/<int:task_id>/setNote', methods=['GET', 'POST'])
def set_note(task_id):
    if request.method == 'POST':
        done = request.get_json(force=True).get('note')
        if done not in [0, 1]:
            response = jsonify({
                "status": "KO"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        try:
            connection = mysql.connector.connect(host='213.32.19.136',
                                                 database='visian',
                                                 user='visian',
                                                 password='visian')
            cursor = connection.cursor()
            cursor.execute("update Tasks set Done = " + str(int(done)) + " where id = " + str(int(task_id)))
            connection.commit()
            response = jsonify({
                "status": "OK"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Error as e:
            print("Error updating data from MySQL table", e)
            response = jsonify({
                "status": "KO"
            })
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")


@app.route('/tasks/<int:task_id>', methods=['GET'])
def task(task_id):
    if request.method == 'GET':
        try:
            connection = mysql.connector.connect(host='213.32.19.136',
                                                 database='visian',
                                                 user='visian',
                                                 password='visian')
            cursor = connection.cursor()
            cursor.execute("select * from TasksFull where id = " + str(int(task_id)))
            records = cursor.fetchall()
            response = jsonify(to_dict(cursor.column_names, records))
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        except Error as e:
            print("Error reading data from MySQL table", e)
            response = jsonify([])
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
                print("MySQL connection is closed")


@app.route('/getProjectsByEntityId/<int:entity_id>')
def get_projects_by_entity_id(entity_id):
    try:
        connection = mysql.connector.connect(host='213.32.19.136',
                                             database='visian',
                                             user='visian',
                                             password='visian')
        cursor = connection.cursor()
        cursor.execute("select * from Projects where entity = " + str(int(entity_id)))
        records = cursor.fetchall()
        records = to_dict(cursor.column_names, records)
        response = jsonify(records)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except Error as e:
        print("Error reading data from MySQL table", e)
        response = jsonify([])
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    app.run()
