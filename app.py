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


@app.route('/dummy')
def dummy():
  return render_template('dummy.html')


@app.route('/buyer_index')
def buyer_index():


  return render_template('buyer_index.html')
@app.route('/agent_layout')
def agent_layout():
  return render_template('agent_layout.html')

@app.route('/login')
def login():
    return render_template('login.html')

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
        return redirect(url_for('agent_layout'))

      else:
        session.clear()
        session['user_id'] = user[0]
        session['user_type'] = user[4]
        flash('Already logged in')
        return redirect(url_for('index'))




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


############################ ##############
##########################################
##########################################
############## Property ###################
############## ############################
##########################################
##########################################
##########################################

def show_properties():
  conn = get_db_connection()
    # psycopg2.connect(database='your_database_name', user='your_database_user', password='your_database_password', host='localhost', port='5432')
  cur = conn.cursor()
  cur.execute('SELECT * FROM property')
  properties = cur.fetchall()
  print(properties)
  conn.close()

  return properties


@app.route('/property_index')
def property_index():
    print('in proooooooooooooppppppppppppppertieeeeeeeeeeesssssssss')
    properties = show_properties()
    return render_template('property_index.html', properties=properties)
    # return render_template('property_index.html')



@app.route('/add_property')
def add_property():
  print('*L' * 10)
  return render_template('add_property.html')

# @app.route('/add_property',  methods=['POST'])
@app.route('/add_property', methods=['POST'])
def insert_property():

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        property_type = request.form['type']
        location = request.form['location']
        agent_id = request.form['agent_id']
        city = request.form['city']
        state = request.form['state']
        description = request.form['description']
        price = request.form['price']
        availability = request.form['availability']
        neighborhood_id = request.form['neighborhood_id']

        # Execute the INSERT statement to add the new property to the database
        cur.execute(
            """INSERT INTO property (type, location, agent_id, city, state, description, price, availability, neighborhood_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);""",
            (property_type, location, agent_id, city, state, description, price, availability, neighborhood_id)
        )

        conn.commit()
        flash('Property added successfully!')

    except Exception as e:
        conn.rollback()
        flash('An error occurred while adding the property. Please try again.')
        print(e)

    finally:
        cur.close()

    return redirect(url_for('agent_layout'))

  #Add neighborhood

@app.route('/add_neighborhood')
def add_neighborhood():
  return render_template('add_neighborhood.html')

@app.route('/add_neighborhood', methods=['POST'])
def insert_neighborhood():

  print('beeeeeeeeeeeeeeeeeeeeeen dpwwwwwwwwwwwwn')
  conn = get_db_connection()
  cur = conn.cursor()
  if request.method == 'POST':
        crime_rate = request.form['crime_rate']
        state = request.form['state']
        city = request.form['city']
        location = request.form['location']

        try:
            cur.execute("INSERT INTO neighborhood (crime_rate, state, city, location) VALUES (%s, %s, %s, %s)", (crime_rate, state, city, location))
            conn.commit()
            flash('Neighborhood added successfully!', 'success')
            return redirect(url_for('add_neighborhood'))
        except Exception as e:
            conn.rollback()
            flash('Error occurred while adding neighborhood', 'error')
            print(str(e))

  return render_template('add_neighborhood.html')


# @app.route('/propety_index', methods=['get'])
# def properties():
    # print('in proooooooooooooppppppppppppppertieeeeeeeeeeesssssssss')
    # conn = get_db_connection()
    # # psycopg2.connect(database='your_database_name', user='your_database_user', password='your_database_password', host='localhost', port='5432')
    # cur = conn.cursor()
    # cur.execute('SELECT * FROM property')
    # properties = cur.fetchall()
    # conn.close()
    # return render_template('property_index.html', properties=properties)





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))






if __name__ == '__main__':
    app.run(debug=True)


