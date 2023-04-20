import os
import psycopg2
from flask import Flask, render_template

app = Flask(__name__, static_url_path='/static', static_folder='static')

def get_db_connection():
    conn = psycopg2.connect(host='localhost',
                            database='test2',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return conn


@app.route('/')
def index():
    print(psycopg2.__version__)
    conn = get_db_connection()
    cur = conn.cursor()
    # cur.execute('GRANT INSERT ON TABLE "agents" TO mak;')
    # cur.execute('SELECT * FROM agents')
    print(os.environ['DB_USERNAME'],os.environ['DB_PASSWORD'])
    cur.execute('SELECT * FROM agents')
    books = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', books=books)
