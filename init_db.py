import os
import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="test2",
        user=os.environ['DB_USERNAME'],
        password=os.environ['DB_PASSWORD'])

print (os.environ['DB_USERNAME'],os.environ['DB_PASSWORD']  )

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# cur.execute('DROP TABLE IF EXISTS books;')
# cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                #  'title varchar (150) NOT NULL,'
                                #  'author varchar (50) NOT NULL,'
                                #  'pages_num integer NOT NULL,'
                                #  'review text,'
                                #  'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                #  )

# Insert data into the table

cur.execute('INSERT INTO "User" (User_ID, Name ,Email ,UserType ,Password)'
'VALUES( %s,%s,%s,%s,%s )',
(4,'test','test@gmail.com','agent','test@123'))

cur.execute('INSERT INTO "agents" (agent_id,user_id ,job_title ,real_estate_agency,contact_information,email)'
            'VALUES(%s,%s,%s,%s,%s,%s)',
            (4,'4','agent','test_agency','811111','test@gmail.com'))



conn.commit()

cur.close()
conn.close()
