from flask import Flask, render_template, request, session, redirect, url_for, escape
from jinja2 import Template
import psycopg2
import config

app = Flask(__name__)

#DATABASE_URL = os.environ['DATABASE_URL']

#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

#app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def student():
   return "config.db"

if __name__ == '__main__':
    app.run()
    #app.run(debug=True, use_reloader=True) 