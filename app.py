import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
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


  # return render_template('buyer_index.html')
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

@app.route('/signup', methods=['POST'])
def signup_post():
    email = request.form['email']
    name = request.form['name']
    password = request.form['password']
    user_type = request.form['user_type']

    user_id = random.randint(0,1230000)
    gen_id = random.randint(0,123)

    print('-------')
    print(name, email, password, type(user_type), user_type, user_id)
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
    conn.commit()

    cur.execute('SELECT user_id FROM "User" WHERE email = %s', (email,))
    user_id = cur.fetchone()[0]

    session.clear()
    session['user_id'] = user_id

    if str(user_type) == "agent":
      real_estate_agency = request.form['real_estate_agency']
      contact_info = request.form['contact_information']
      cur.execute('INSERT INTO agents (agent_id, user_id, job_title, real_estate_agency, contact_information, email) VALUES (%s, %s, %s, %s, %s, %s)', (gen_id, user_id, user_type, real_estate_agency, contact_info, email))
      conn.commit()
      return redirect(url_for('property_index'))

    else:
      cur.execute('INSERT INTO renters (renter_id, user_id, email) VALUES (%s, %s, %s)', (gen_id, user_id, email))
      conn.commit()
      return redirect(url_for('buyer_index'))


    # conn.commit()

    # cur = conn.cursor()

    # # cur.execute("SELECT user_id FROM "User" WHERE email = %s", (email,))
    # cur.execute('SELECT user_id, password, name, email, usertype FROM "User" WHERE email = %s', (email,))
    # existing_user = cur.fetchone()

    # if existing_user is not None:
    #     flash('Email address already in use.')
    #     return redirect(url_for('signup'))

    # # password_hash = generate_password_hash(password)

    # cur.execute('INSERT INTO "User" (user_id, name, email, password, usertype) VALUES (%s, %s, %s, %s, %s)', (user_id, name, email, password, user_type))

    # # session.clear()

    # cur.execute('SELECT user_id FROM "User" WHERE email = %s', (email,))
    # user_id = cur.fetchone()[0]
    # session['user_id'] = user_id

    # if str(user_type) == "agent":
    #   real_estate_agency = request.form['real_estate_agency']
    #   contact_info = request.form['contact_information']
    #   cur.execute('INSERT INTO agents (agent_id, user_id, job_title, real_estate_agency, contact_information, email) VALUES (%s, %s, %s, %s, %s, %s)', (gen_id, user_id, user_type, real_estate_agency, contact_info, email))
    #   conn.commit()
    #   return redirect(url_for('property_index'))
    # else:
    #   cur.execute('INSERT INTO renters (renter_id, user_id, email) VALUES (%s, %s, %s)', (gen_id, user_id, email))
    #   return redirect(url_for('buyer_index'))


    # session.clear()
    # session['user_id'] = user_id




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

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT agent_id FROM agents WHERE user_id=%s', (session['user_id'],))
    agent_id = cur.fetchone()

    print(type(agent_id[0]), 'hurrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')



    properties = show_properties()
    print(properties)
    return render_template('property_index.html', properties=properties, agent_id=agent_id[0])



@app.route('/add_property')
def add_property():
  return render_template('add_property.html')

@app.route('/add_property', methods=['POST'])
def insert_property():

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        property_type = request.form['type']
        location = request.form['location']
        # agent_id = request.form['agent_id']
        city = request.form['city']
        state = request.form['state']
        description = request.form['description']
        price = request.form['price']
        availability = request.form['availability']
        neighborhood_id = request.form['neighborhood_id']

        cur.execute('SELECT agent_id FROM agents WHERE user_id=%s', (session['user_id'],))
        agent_id = cur.fetchone()

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

    return redirect(url_for('property_index'))

@app.route('/view_property/<int:id>', methods=['GET', 'POST'])
def view_property(id):
  print('hi', id)
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute("SELECT * FROM property WHERE property_id = %s", (id,))
  property = cur.fetchone()

  cur.execute('SELECT agent_id FROM agents WHERE user_id=%s', (session['user_id'],))
  agent_id = cur.fetchone()[0]

  print(property, 'yo baby')

  return render_template('view_property.html', property=property, agent_id=agent_id)


@app.route('/view_booking_property/<int:id>', methods=['GET', 'POST'])
def view_booking_property(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT agent_id FROM agents WHERE user_id=%s', (session['user_id'],))
    agent_id = cur.fetchone()[0]

    cur.execute('SELECT * FROM propertybooking WHERE propertyid=%s', (id,))
    bookings = cur.fetchall()

    print(bookings, 'this is boooooo..........///////oooooooooooookings',agent_id)
    # if agent_id == bookings[7]:
    return render_template('view_booking_history.html', bookings=bookings)
    # else:
    #     return render_template('error.html', message='You do not have permission to view this booking history.')

@app.route('/delete_booking_agent/<int:propertybookingid>', methods=['GET', 'POST'] )
def delete_booking_agent(propertybookingid):
  try:
      conn = get_db_connection()
      cur = conn.cursor()
      cur.execute("DELETE FROM propertybooking WHERE propertybookingid = %s", (propertybookingid,))
      conn.commit()
      print("Booking deleted successfully.")
  except psycopg2.Error as e:
      print("Error deleting booking:", e)
  finally:
      cur.close()
      conn.close()

  return redirect(url_for('property_index'))




@app.route('/modify_property/<int:id>', methods=['GET', 'POST'])
def modify_property(id):

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM property WHERE property_id = %s", (id,))
    property_data = cur.fetchone()

    if request.method == 'POST':
          property_type = request.form['type']
          location = request.form['location']
          # agent_id = id
          city = request.form['city']
          state = request.form['state']
          description = request.form['description']
          price = request.form['price']
          availability = request.form['availability']
          neighborhood_id = request.form['neighborhood_id']

          cur.execute('SELECT agent_id FROM agents WHERE user_id=%s', (session['user_id'],))
          agent_id = cur.fetchone()[0]

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
      return redirect(url_for('property_index'))
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
  # print('NOOOOOOOOOOOOOOOOOOOOOONONONNNNNNNNNNNNNNNNNNNNWS')
  # print('NOOOOOOOOOOOOOOOOOOOOOONONONNNNNNNNNNNNNNNNNNNNWS')

  return render_template('renter_profile.html')

@app.route('/renter_add_address', methods=['get'])
def renter_add_address():
  # print('in renter adddd addressssss')
  return render_template('renter_add_address.html')

@app.route('/renter_add_address',methods=['POST'])
def renter_insert_address():
  # print('hryy we in insert add addresssss')

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
    return redirect(url_for('buyer_index'))

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

@app.route('/add_credit_card', methods=['GET', 'POST'])
def add_credit_card():
  conn = get_db_connection()
  cur = conn.cursor()
  # cur.execute('SELECT * FROM address WHERE user_id=%s', (session['user_id']))
  cur.execute('SELECT * FROM address WHERE user_id=%s', (session['user_id'],))


  addresses = cur.fetchall()

  if request.method == 'POST':
        print('we in add_credit_card_post', request.form['paymentaddress_id'][0])
        # Get the credit card details from the form
        card_number = request.form['cardnumber']
        expiration_date = request.form['expirationdate']
        cvv = request.form['cvv']

        # Get the payment address ID from the database for the renter
        cur.execute('SELECT renter_id FROM renters WHERE user_id=%s', (session['user_id'],))
        renter_id = cur.fetchone()

        # cur.execute('SELECT paymentaddress_id FROM renters WHERE renter_id = %s', (session['user_id'],))
        payment_address_id = request.form['paymentaddress_id'] #cur.fetchone()[0]

        print('we in add_credit_card_post@', payment_address_id, cvv, expiration_date)

        # Insert the credit card details into the database
        cur.execute('INSERT INTO creditcard (renter_id, cardnumber, expirationdate, paymentaddress_id, cvv) VALUES (%s, %s, %s, %s, %s)', (renter_id, card_number, expiration_date, payment_address_id, cvv))
        conn.commit()
        conn.close()

        flash('Credit card added successfully!', 'success')
        return redirect(url_for('renter_profile'))

  else:
      return render_template('add_creditcard.html', addresses=addresses)


@app.route('/creditcards')
def creditcards():
  # renter_id = db.session.query(renters.renter_id).filter_by(user_id=session['user_id']).scalar()
  # cur = db.cursor()
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute('SELECT renter_id FROM renters WHERE user_id=%s', (session['user_id'],))
  renter_id = cur.fetchone()


  cur.execute('SELECT * FROM creditcard WHERE renter_id=%s', (renter_id,))
  creditcards = cur.fetchall()
  cur.close()
  return render_template('creditcards.html', creditcards=creditcards)


@app.route('/delete_creditcard/<int:credit_cardid>', methods=['POST', 'get'])
def delete_creditcard(credit_cardid):
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute('DELETE FROM creditcard WHERE credit_cardid = %s', (credit_cardid,))
  conn.commit()
  flash('Credit Card deleted successfully!', 'success')
  conn.close()
  # return redirect(url_for('show_addresses'))
  return redirect(url_for('renter_profile'))

@app.route('/modify_creditcard/<int:credit_cardid>', methods=['POST', 'get'])
def modify_creditcard(credit_cardid):

  conn = get_db_connection()
  cur = conn.cursor()

  # cur.execute('SELECT renter_id FROM renters WHERE user_id = %s', (session['user_id'] )
  cur.execute('SELECT renter_id FROM renters WHERE user_id = %s', [session['user_id']])

  renter_id = cur.fetchone()

  cur.execute('SELECT * FROM creditcard WHERE credit_cardid=%s AND renter_id=%s', (credit_cardid, renter_id))
  creditcard = cur.fetchone()

    # Check if the credit card belongs to the current user
  if creditcard is None:
      return "Credit card not found", 404
    # Check if the request method is POST
  elif request.method == 'POST':
    # Retrieve the form data
    cardnumber = request.form['cardnumber']
    expirationdate = request.form['expirationdate']
    paymentaddress_id = request.form['paymentaddress_id']
    cvv = request.form['cvv']
    # Update the credit card in the database
    cur.execute('UPDATE creditcard SET cardnumber=%s, expirationdate=%s, paymentaddress_id=%s, cvv=%s WHERE credit_cardid=%s', (cardnumber, expirationdate, paymentaddress_id, cvv, credit_cardid))

    # cur.execute('UPDATE creditcard SET cardnumber=%s, expirationdate=%s, paymentaddress_id=%s, cvv=%s WHERE credit_cardid=%s', (cardnumber, expirationdate, paymentaddress_id, cvv, credit_cardid))
    conn.commit()
    # Redirect to the credit card list page
    return redirect(url_for('creditcards'))
    # Otherwise, render the credit card edit form
  else:
      cur.execute('SELECT * FROM address WHERE user_id=%s', (session['user_id'],))
      addresses = cur.fetchall()
      return render_template('modify_creditcard.html', creditcard=creditcard, addresses=addresses)

@app.route('/book_property/<int:id>', methods=['GET'])
def book_property(id):
  conn = get_db_connection()
  cur = conn.cursor()
  # renturn
  cur.execute('SELECT renter_id FROM renters WHERE user_id=%s', (session['user_id'],))
  renter_id = cur.fetchone()

  cur.execute('SELECT * FROM creditcard WHERE renter_id=%s', (renter_id,))
  creditcards = cur.fetchall()

  cur.execute('SELECT * FROM address WHERE user_id=%s', (session['user_id'], ))
  addresses = cur.fetchall()

  print(creditcards, renter_id)
  return render_template('make_payment.html', id=id, creditcards=creditcards, addresses=addresses)


  # return render_template('modify_address.html', address=address)
@app.route('/book_property/<int:id>', methods=['POST'])
def make_payment(id):

  print('make payment')
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute('SELECT * FROM property WHERE property_id=%s', (id, ))
  property = cur.fetchone()

  cur.execute('SELECT renter_id FROM renters WHERE user_id=%s', (session['user_id'], ))
  renter_id = cur.fetchone()


  print(property)

  if request.method == 'POST':
    print('make payment we gon make it thruuuuuuuuuuuu')


    credit_card_id = request.form['credit_card_id']
    # print(credit_card_id)
    days_of_stay = request.form['days_of_stay']

    today = date.today().strftime('%Y-%m-%d')

    address = request.form['address_id']
    # calculate payment_amount
    payment_amount = int(property[6]) * int(days_of_stay)
    print(property[6], 'hey')
    print(property)

    cur.execute('INSERT INTO payment(payment_status, credit_card_id, renter_id, propertyid, agent_id, date, payment_amount) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (False, credit_card_id, renter_id, id, property[9], today, payment_amount))
    conn.commit()

    address = request.form['address_id']
    desired_move_in_date = request.form['desired_move_in_date']

    # cur.execute('INSERT INTO propertybooking(renter_id, propertyid, creditcardid, desired_move_in_date, billingaddress_id, budget, agentid) VALUES (%s, %s, %s, %s, %s, %s)',
                    # (renter_id, id, credit_card_id, desired_move_in_date, address, payment_amount,property[8]))
    cur.execute('INSERT INTO propertybooking(renter_id, propertyid, creditcardid, desired_move_in_date, billingaddress_id, budget, agentid) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                    (renter_id, id, credit_card_id, desired_move_in_date, address, payment_amount,property[9]))

    conn.commit()

    # update property availability
    cur.execute('UPDATE property SET availability = %s WHERE property_id = %s', (False, id))
    conn.commit()

    # update payment status
    cur.execute('UPDATE payment SET payment_status = %s WHERE propertyid = %s', (True, id))
    conn.commit()


  print('payment_amount', payment_amount, address, desired_move_in_date, 'heyyyyyyyyyyyyyyyyyyyyyy' )
  print('this is property', property)
  print(days_of_stay, 'days_of_stay')
  print('this is renter_id' , renter_id)

  return redirect(url_for('buyer_index'))


@app.route('/search')
def search():
  print('in search')
  return render_template('search.html');

@app.route('/search_property',  methods=['post'])
def search_property():
  conn = get_db_connection()
  cur = conn.cursor()

  # if request.method == 'post' or 'get':
  print('dekh le tu, aajazi ye meri')
#        # Get search criteria from the form
  print(len(request.form))
  print(request.form['location'])

  location = request.form['location']
  # date = request.form['date']
  # availability = request.form['availability']
  # min_bedrooms = request.form['min_bedrooms']
  # max_price = request.form['max_price']
  # property_type = request.form['property_type']
  # order_by = request.form['order_by']

  print(request.form['date'])
  print(request.form['min_price'])
  # print(min_bedrooms)
  # print(max_price)
  # print(property_type, 'lplplplpl')
  # print(order_by)

  cur = conn.cursor()
  # cur.execute('UPDATE payment SET payment_status = %s WHERE propertyid = %s', (True, id))

  # cur.execute('SELECT * FROM property where city=%s', location)
  cur.execute('SELECT * FROM property WHERE city=%s', (location,))

  properties = cur.fetchall()
  # print('location', sql)
  print(properties)

  return render_template('search_results.html', properties=properties)

@app.route('/mybooking')
def mybooking():
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute('SELECT renter_id FROM renters WHERE user_id=%s', (session['user_id'],))
  renter_id = cur.fetchone()

  cur.execute('SELECT * FROM propertybooking WHERE renter_id = %s', (renter_id,))
  bookings = cur.fetchall()

  print(bookings)
  return render_template('mybooking.html', bookings=bookings)



@app.route('/deletebooking/<int:propertybookingid>', methods=['GET', 'POST'] )
def delete_booking(propertybookingid):
  try:
      conn = get_db_connection()
      cur = conn.cursor()
      cur.execute("DELETE FROM propertybooking WHERE propertybookingid = %s", (propertybookingid,))
      conn.commit()
      print("Booking deleted successfully.")
  except psycopg2.Error as e:
      print("Error deleting booking:", e)
  finally:
      cur.close()
      conn.close()

  return redirect(url_for('mybooking'))



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))






if __name__ == '__main__':
    app.run(debug=True)


