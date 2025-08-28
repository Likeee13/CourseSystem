from flask import Flask, request, jsonify
import sqlite3

import db_init

app = Flask(__name__)

def get_db_connection():
    return sqlite3.connect('CourseSystem.db')

@app.route('/execute', methods=['POST'])
def handle_query():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(data['query'], tuple(data['params']))
        result = cursor.fetchall()
        conn.commit()
        return jsonify({
            "status": "success",
            "data": result
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    #db_init.init_db()
    #app.run(host="localhost", port=5000,debug=True)
    app.run(host="10.29.23.222", port=5000)  # 允许局域网访问