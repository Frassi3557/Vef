#from config import config
#import psycopg2

#@app.route('/delete')
#def delete():
#    delete = "DELETE FROM users"
#    conn = None
#    try:
#        # read the connection parameters
#        params = config()
#        # connect to the PostgreSQL server
#        conn = psycopg2.connect(**params)
#        cur = conn.cursor()
#        # create table one by one
#        cur.execute(delete)
#        # close communication with the PostgreSQL database server
#        cur.close()
#        # commit the changes
#        conn.commit()
#    except (Exception, psycopg2.DatabaseError) as error:
#        print(error)
#    finally:
#        if conn is not None:
#            conn.close()
#
#    
#def create_tables():
#    """ create tables in the PostgreSQL database"""
#    commands = (
#        """
#        CREATE TABLE users (
#            name VARCHAR(50) NOT NULL,
#            username VARCHAR(32) NOT NULL,
#            passw VARCHAR(32) NOT NULL
#        )
#        """)
#    conn = None
#    try:
#        # read the connection parameters
#        params = config()
#        # connect to the PostgreSQL server
#        conn = psycopg2.connect(**params)
#        cur = conn.cursor()
#        # create table one by one
#        cur.execute(commands)
#        # close communication with the PostgreSQL database server
#        cur.close()
#        # commit the changes
#        conn.commit()
#    except (Exception, psycopg2.DatabaseError) as error:
#        print(error)
#    finally:
#        if conn is not None:
#            conn.close()

    #if request.method == 'POST':
    #    session['username'] = request.form['username']
    #    session['password'] = request.form['passw']
    #    return redirect(url_for('login'))


#    REATE TABLE notendur (
#            userid INT NOT NULL PRIMARY KEY, 
#           name VARCHAR(50) NOT NULL,
#           username VARCHAR(32) NOT NULL,
#           passw VARCHAR(32) NOT NULL


#        CREATE TABLE grein (
#            articleid INT NOT NULL, 
#            title VARCHAR(50) NOT NULL,
#            content VARCHAR(500) NOT NULL,
#            img VARCHAR NOT NULL,
#            userid INT,
#            PRIMARY KEY (articleid),
#            FOREIGN KEY (userid) REFERENCES notendur(userid)
#        )     
