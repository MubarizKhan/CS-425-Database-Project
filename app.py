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
  print('in buyer index')
  properties = show_properties()
  return render_template('buyer_index.html', properties=properties)


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
      session['user_id'] = user[0]
      session['user_type'] = user[4]
      if session.get('user_id') and session['user_id'] == user[0] and session['user_type'] == 'agent':
        return redirect(url_for('property_index'))

      else:
        return redirect(url_for('buyer_index'))
        # session.clear()
        # session['user_id'] = user[0]
        # session['user_type'] = user[4]
        # flash('Already logged in')
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

############################ ##############
##########################################
##########################################
############## AGENTS ###################
############## ############################
##########################################
##########################################
##########################################
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



@app.route('/add_property')
def add_property():
  print('*L' * 10)
  return render_template('add_property.html')

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


@app.route('/modify_property/<int:id>', methods=['GET', 'POST'])
def modify_property(id):
    # Your code here
    print('its hitting' * 10)
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM property WHERE property_id = %s", (id,))
    property_data = cur.fetchone()

    if request.method == 'POST':
          property_type = request.form['type']
          location = request.form['location']
          agent_id = id
          city = request.form['city']
          state = request.form['state']
          description = request.form['description']
          price = request.form['price']
          availability = request.form['availability']
          neighborhood_id = request.form['neighborhood_id']

          try:

              cur.execute("UPDATE property SET type = %s, location = %s, agent_id = %s, city = %s, state = %s, description = %s, price = %s, availability = %s, neighborhood_id = %s WHERE property_id = %s", (property_type, location, agent_id, city, state, description, price, availability, neighborhood_id, id))
              conn.commit()
              flash('Property modified successfully!', 'success')
              return redirect(url_for('modify_property'))
          except Exception as e:
              conn.rollback()
              flash('Error occurred while modifying property', 'error')
              print(str(e))
    return render_template('modify_property.html')

@app.route('/delete_property/<int:id>', methods=['get'])
def delete_property(id):

  print(' weeeeeeeeeeeeee deleting', session['user_id'])
  conn = get_db_connection()
  cur = conn.cursor()

  # Check if the property's agent_id matches the id of the current user
  cur.execute('SELECT agent_id FROM property WHERE property_id=%s', (id,))
  result = cur.fetchone()
  print(result[0])
  print(result, 'this is result' * 5)
  print(result[0], session['user_id'])


  cur.execute('SELECT user_id,agent_id FROM agents WHERE agent_id=%s', (result[0],))
  session_user_id = cur.fetchone()
  print(session_user_id, 'TTHIS IS SESSION USER' * 2)

  if not session_user_id or session_user_id[0] != session['user_id']:
      flash('You are not authorized to delete this property.', 'error')
      return redirect(url_for('dummy'))
  try:
      # Delete the property from the database
      cur.execute('DELETE FROM property WHERE property_id=%s', (id,))
      conn.commit()
      flash('Property deleted successfully!', 'success')
  except Exception as e:
      conn.rollback()
      flash('Error occurred while deleting property', 'error')
      print(str(e))
  finally:
      conn.close()
  # return redirect(url_for('home'))
  return render_template('property_index.html')




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


############################ ##############
##########################################
##########################################
############## RENTERS ###################
############## ############################
##########################################
##########################################
##########################################
############################ ##############
##########################################
##########################################
############## Addressess ###################
############## ############################
##########################################
##########################################
##########################################


@app.route('/renter_profile')
def renter_profile():
  print('NOOOOOOOOOOOOOOOOOOOOOONONONNNNNNNNNNNNNNNNNNNNWS')
  print('NOOOOOOOOOOOOOOOOOOOOOONONONNNNNNNNNNNNNNNNNNNNWS')

  return render_template('renter_profile.html')

@app.route('/renter_add_address', methods=['get'])
def renter_add_address():
  print('in renter adddd addressssss')
  return render_template('renter_add_address.html')

@app.route('/renter_add_address',methods=['POST'])
def renter_insert_address():
  print('hryy we in insert add addresssss')

  if request.method == 'POST':
    conn = get_db_connection()
    cur = conn.cursor()
    # Retrieve user_id from session
    user_id = session['user_id']
    # Retrieve data from the form
    address = request.form['address']
    state = request.form['state']
    city = request.form['city']
    zip_code = request.form['zip_code']

    cur.execute('INSERT INTO address (user_id, address, state, city, zip_code) VALUES (%s, %s, %s, %s, %s)',
                  (user_id, address, state, city, zip_code))
    conn.commit()

    # Close the database connection
    conn.close()

    # Redirect to the user's profile page
    return redirect(url_for('renter_add_address'))

@app.route('/all_renters_addresses', methods=['GET', 'POST'])
def all_renters_addresses():
  conn = get_db_connection()
  cur = conn.cursor()
  # Get all addresses belonging to the current user
  cur.execute('SELECT * FROM address WHERE user_id=%s', (session['user_id'],))
  addresses = cur.fetchall()

  conn.close()

  return render_template('all_renters_addresses.html', addresses=addresses)

@app.route('/modify_address/<int:address_id>', methods=['GET', 'POST'])
def modify_address(address_id):
  conn = get_db_connection()
  cur = conn.cursor()
  # Get the address associated with the given address_id
  cur.execute('SELECT * FROM address WHERE address_id=%s AND user_id=%s', (address_id, session['user_id']))
  address = cur.fetchone()
  # If the address doesn't exist or doesn't belong to the current user, redirect to the home page
  if not address:
      conn.close()
      flash('Address not found.', 'error')
      return redirect(url_for('home'))

  if request.method == 'POST':
      # Update the address in the database
      new_address = request.form['address']
      new_city = request.form['city']
      new_state = request.form['state']
      new_zip_code = request.form['zip_code']
      cur.execute('UPDATE address SET address=%s, city=%s, state=%s, zip_code=%s WHERE address_id=%s',
                  (new_address, new_city, new_state, new_zip_code, address_id))
      conn.commit()
      flash('Address updated successfully!', 'success')
      conn.close()
      return redirect(url_for('renter_profile'))
  conn.close()

  return render_template('modify_address.html', address=address)


@app.route('/delete_address/<int:address_id>', methods=['GET', 'POST'])
def delete_address(address_id):
  conn = get_db_connection()
  cur = conn.cursor()
  cur.execute('DELETE FROM address WHERE address_id = %s', (address_id,))
  conn.commit()
  flash('Address deleted successfully!', 'success')
  conn.close()
  # return redirect(url_for('show_addresses'))
  return redirect(url_for('renter_profile'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))






if __name__ == '__main__':
    app.run(debug=True)


