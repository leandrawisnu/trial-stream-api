from flask import Flask, Response, stream_with_context, send_from_directory
from flask_cors import CORS
import psycopg2
import json
import os
import time

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    print("Serving index.html")
    return send_from_directory(os.getcwd(), 'stream.html')

def get_db_connection():
    return psycopg2.connect("dbname=stream-api user=postgres password=password host=localhost")

@app.route('/stream')
def stream_people():
    def generate():
        conn = get_db_connection()
        cursor = conn.cursor()
        batch_size = 1
        offset = 0
        total_sent = 0

        while True:
            cursor.execute("""
                SELECT pk, sk, fname, lname, dob, zipcode
                FROM people
                ORDER BY pk
                LIMIT %s OFFSET %s
            """, (batch_size, offset))

            rows = cursor.fetchall()
            if not rows:
                break

            for idx, row in enumerate(rows):
                # Check if there are more rows by peeking ahead
                cursor.execute("SELECT COUNT(*) FROM people WHERE pk > %s", (row[0],))
                has_more = cursor.fetchone()[0] > 0
                
                person = {
                    "pk": row[0],
                    "sk": row[1],
                    "fname": row[2],
                    "lname": row[3],
                    "dob": str(row[4]),
                    "zipcode": row[5],
                    "last_row": not has_more or total_sent >= 999,
                }
                yield f"data: {json.dumps(person)}\n\n"
                total_sent += 1
                
                if total_sent >= 1000:
                    break

            offset += batch_size
            
            if total_sent >= 1000:
                break

        cursor.close()
        conn.close()

    return Response(stream_with_context(generate()), mimetype='text/event-stream', headers={'Access-Control-Allow-Origin': '*'})


if __name__ == '__main__':
    print("Starting server at http://localhost:5000/")
    app.run(host='0.0.0.0', port=5000, debug=True)