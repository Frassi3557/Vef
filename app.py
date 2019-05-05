from flask import Flask, render_template, request, session, redirect, url_for, escape
from jinja2 import Template
import psycopg2
from config import config
import requests
import json
import urllib.request

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

with urllib.request.urlopen('https://apis.is/petrol') as url:
    gogn = json.loads(url.read().decode())
    print(gogn)

@app.route('/mid')
def indexmid():
    return render_template("result.html", gogn = gogn)

@app.route('/mid/stations')
def stations():
    return render_template("stations.html", gogn = gogn)

@app.route('/')
def index7():
    if 'username' in session:
        return redirect(url_for('users'))
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index7'))

@app.route('/login', methods = ['GET','POST'])
def login():
    #if 'username' and 'password' in session:
    if request.method == 'POST':
        session['username'] = request.form['username']
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
            print(cur.execute(sql,(user, password)))
            #cur.execute(sqluserlist)
            users = cur.fetchone()
            #userlist = cur.fetchall()
            if user == users[1] and password == users[2]:
                print(users[0])
                print(users[1])
                print(users[2])
                return redirect(url_for("users"))
            else:
                return render_template("wrong.html")
            #conn.commit()
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return render_template("wrong.html")
        finally:
            if conn is not None:
                conn.close()
                #cur.close()
        #return redirect(url_for('users'))
        #return render_template("index.html", users = users, userlist = userlist)
    else:
        return redirect(url_for('index7'))

@app.route('/insert')
def insert():
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
            return error
        finally:
            if conn is not None:
                conn.close()
        return redirect(url_for('index7'))
    else:
        return redirect(url_for('index7'))

@app.route('/create' , methods = ['GET', 'POST'])
def create():
    if 'username' in session:
        user = session['username']
        sql = "SELECT username from users WHERE username='{}'".format(user)
        print(sql)
        conn = None
        try:
            # read database configuration
            params = config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the INSERT statement
            cur.execute(sql)
            result = cur.fetchone()
            sqluser = "('" + user + "',)"
            print(sqluser)
            print(result)   
            if(result == None):
                return redirect(url_for('insert'))
            else:
                return render_template("exists.html")
            # close communication with the database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            return error
        finally:
            if conn is not None:
                conn.close()
    return 'username not in session'

@app.route('/register' , methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['username'] = request.form['username']
        session['password'] = request.form['passw']
        return redirect(url_for('create'))
    return render_template("register.html")

@app.route('/users')
def users():
    if 'username' in session:
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
    return redirect(url_for('index7'))

if __name__ == '__main__':
    app.run()