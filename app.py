from flask import Flask, render_template, request, session, redirect, url_for, escape
from jinja2 import Template
import psycopg2
from config import config
import requests

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index7():
    #if request.method == 'POST':
    #    session['username'] = request.form['username']
    #    session['password'] = request.form['passw']
    #    return redirect(url_for('login'))
    return '''
        <form action="/login" method="POST">
            <p>Notendanafn: </p><input type=text name=username required>
            <p>Lykilorð: </p><input type=password name=passw required>
            <p><input type=submit value=Log-in>
        </form>
    '''

@app.route('/login', methods = ['GET','POST'])
def login():
    #if 'username' and 'password' in session:
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['passw']
        sql = "SELECT name,username,passw FROM users WHERE username=%s AND passw=%s"
        #sqluserlist = "SELECT name,username FROM users"
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql,(user, password))
            #cur.execute(sqluserlist)
            # commit the changes to the database
            users = cur.fetchone()
            userlist = cur.fetchall()
            if user == users[1] and password == users[2]:
                print(users[0])
                print(users[1])
                print(users[2])
                return redirect(url_for("users"))
            else:
                return redirect(url_for('index7'))
            print(users[0])
            print(users[1])
            #conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
                #cur.close()
        #return redirect(url_for('users'))
        #return render_template("index.html", users = users, userlist = userlist)
    return '''render_template("index.html", verify = verify)'''

@app.route('/create' , methods = ['GET', 'POST'])
def create():
    if 'name' and 'username' and 'password' in session:
        user = session['username']
        name = session['name']
        password = session['password']
        sql = "INSERT INTO users(name, username, passw) VALUES(%s, %s, %s)"
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql,(name, user, password))
            # commit the changes to the database
            conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return redirect(url_for('index7'))
    return redirect(url_for('register'))

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['username'] = request.form['username']
        session['password'] = request.form['passw']
        return redirect(url_for('create'))
    return '''
        <form method="POST">
            <p>Nafn: </p><input type=text name=name required>
            <p>Notendanafn: </p><input type=text name=username required>
            <p>Lykilorð: </p><input type=password name=passw required>
            <p><input type=submit value=Register>
        </form>
    '''

@app.route('/users')
def users():
    sql = "SELECT * FROM users"
    conn = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statemendt
        cur.execute(sql)
        users = cur.fetchall()
        #for row in users:
        #    print(row[0])
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()
        return render_template("index.html",users = users)
    return """render_template("index.html",users = users)"""

if __name__ == '__main__':
    app.run()

    
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