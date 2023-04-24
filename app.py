import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import random


app = Flask(__name__, static_url_path='/static', static_folder='static')
app.config['SECRET_KEY'] = 'mysecretkey'


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
    print(os.environ['DB_USERNAME'],os.environ['DB_PASSWORD'])
    cur.execute('SELECT * FROM agents')
    agents = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', agents=agents)

# app.route('/yummy/')
# def dummy():
#   return render_template('dummy.html')

@app.route('/dummy')
def dummy():
  return render_template('dummy.html')


@app.route('/buyer_index')
def buyer_index():
  return render_template('buyer_index.html')

@app.route('/login')
def login():
    return render_template('login.html')

# ')
# @app.route('logout')
# def logout():
#   return render_template('index.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password_hash = request.form['password']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT user_id, password, name, email, usertype FROM "User" WHERE email = %s', (email,))

    user = cur.fetchone()

    if user is None:
      flash('Invalid email or password.')
      return redirect('/login')

    else:
      if session.get('user_id') and session['user_id'] == user[0]:
        return redirect(url_for('dummy'))

      else:
        session.clear()
        session['user_id'] = user[0]
        session['user_type'] = user[4]
        flash('Already logged in')
        return redirect(url_for('index'))



    # user_id, password_hash = user

    # if not check_password_hash(password_hash, password):
    #     flash('Invalid email or password.')
    #     return redirect(url_for('login'))

    # session.clear()
    # session['user_id'] = user[0]
    # session['user_type'] = user[4]

    # print('(((((((' * 10)
    # print(user)
    # print(')))))' * 10)

    # return redirect(url_for('index'))


@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    user_type = request.form['user_type']

    user_id = random.randint(0,123)
    gen_id = random.randint(0,123)

    print('-------')
    print(name, email, password, type(user_type), user_type)
    print('======')

    conn = get_db_connection()
    cur = conn.cursor()

    # cur.execute("SELECT user_id FROM "User" WHERE email = %s", (email,))
    cur.execute('SELECT user_id, password, name, email, usertype FROM "User" WHERE email = %s', (email,))
    existing_user = cur.fetchone()

    if existing_user is not None:
        flash('Email address already in use.')
        return redirect(url_for('signup'))

    # password_hash = generate_password_hash(password)

    cur.execute('INSERT INTO "User" (user_id, name, email, password, usertype) VALUES (%s, %s, %s, %s, %s)', (user_id, name, email, password, user_type))


    if str(user_type) == "agent":
      real_estate_agency = request.form['real_estate_agency']
      contact_info = request.form['contact_information']
      cur.execute('INSERT INTO agents (agent_id, user_id, job_title, real_estate_agency, contact_information, email) VALUES (%s, %s, %s, %s, %s, %s)', (gen_id, user_id, user_type, real_estate_agency, contact_info, email))
    else:
      cur.execute('INSERT INTO renters (renter_id, user_id, email) VALUES (%s, %s, %s)', (gen_id, user_id, email))

    cur.execute('SELECT user_id FROM "User" WHERE email = %s', (email,))
    user_id = cur.fetchone()[0]

    session.clear()
    session['user_id'] = user_id

    conn.commit()
    return redirect(url_for('index'))


@app.route('/add_property')
def add_property():
  print('*L' * 10)
  return render_template('add_property.html')
  # return redirect(url_for('add_property'))

# @app.route('/add_property',  methods=['POST'])
@app.route('/add_property/', methods=['POST'])
def insert_property():

  print('heyyyyyyyyyyyyyyyyyyyy')
  # print(request.form)
  type = request.form['type']
  location = request.form['location']
  # city = request.form['city']
  # state = request.form['state']
  # description = request.form['description']
  # price = request.form['price']
  available = request.form['available']
  neighborhood_id = request.form['neighborhood_id']
  agent_id = request.form['agent_id']

  print(type, location, available, agent_id, neighborhood_id)
  # print('we here')



  # name = request.form['name']
  # password = request.form['password']
  # user_type = request.form['user_type']
  # return render_template('index.html')
  return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))






if __name__ == '__main__':
    app.run(debug=True)


