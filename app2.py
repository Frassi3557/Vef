import psycopg2
from config import config

def create_table():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE notendur(
            userid INT NOT NULL PRIMARY KEY AUTO INCREMENT, 
            name VARCHAR(50) NOT NULL,
            username VARCHAR(32) NOT NULL,
            passw VARCHAR(32) NOT NULL
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

import os
from flask import Flask, flash, redirect, render_template, request, url_for, make_response, escape, session, abort
import pymysql

app = Flask(__name__)
app.secret_key = os.urandom(16)   
print(os.urandom(16))
# https://pythonspot.com/login-authentication-with-flask/

conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='gjg', password='mypassword', database='gjg_vef2vf_19v')

@app.route('/')
def index():
    cur = conn.cursor()
    resultValue = cur.execute("SELECT postur FROM gjg_vef2vf_19v.posts;") 
    if  resultValue > 0:
        userDetails = cur.fetchall()
        flash('Velkomin')
        return render_template('index.tpl',userDetails=userDetails)

@app.route('/nyskraning')
def nyskra():
    if not session.get('logged_in'):
        return render_template('nyskraning.tpl')
    else:
        return render_template('users.tpl')

@app.route('/innskraning')
def innskr():
    if not session.get('logged_in'):
        return render_template('innskraning.tpl')
    else:
        return render_template('users.tpl')

@app.route('/nyskra', methods=['GET', 'POST'])
def nyr():
    if not session.get('logged_in'):
        return render_template('innskraning.tpl')
    else:
        session['logged_in'] = True
    error = None
    if  request.method == 'POST':
        userDetails = request.form
        user = userDetails['userID']
        name = userDetails['user_name']
        email = userDetails['user_email']
        password = userDetails['user_password']
        github = userDetails['user_git']

        try:        
            cur = conn.cursor()
            cur.execute("INSERT INTO gjg_vef2vf_19v.users(userID, nafn, email, pass, github) VALUES(%s, %s, %s, %s, %s)",(user, name, email, password, github))
            conn.commit()
            cur.close()
            flash('Nýskráning tókst og þú ert skráður í gagnagrunninn!')
            return render_template('users.tpl')       # return redirect(url_for('users')) 
        except pymysql.IntegrityError:
            error = 'Notandi er þegar skráður með þessu nafni og/eða lykilorði'  
    return render_template('nyskraning.tpl', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = request.form.get('userID')
        psw = request.form.get('user_password')

        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='gjg', password='mypassword', database='gjg_vef2vf_19v')
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM gjg_vef2vf_19v.users where userID=%s AND pass=%s",(user,psw))
        result = cur.fetchone() #fáum tuple -fetchone

        # er user og psw til í db?
        if result[0] == 1:
            cur.close()
            conn.close()
            flash('Innskráning tókst ')
            session['logged_in'] = True
            return render_template('users.tpl',user=user)
            #return redirect(url_for('users'))
        else:
            error = 'Innskráning mistókst - reyndu aftur'
    return render_template('innskraning.tpl', error=error)

@app.route('/new_post', methods=['GET', 'POST'])
def news():
    if not session.get('logged_in'):
        return render_template('innskraning.tpl')
    else:
        session['logged_in'] = True
    error = None
    if request.method == 'POST':
        pi = request.form.get('postID')
        po = request.form.get('postur')
        ui = request.form.get('userID')

        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='gjg', password='mypassword', database='gjg_vef2vf_19v')
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM gjg_vef2vf_19v.users WHERE userID=%s",(ui))
        result = cur.fetchone() #fáum tuple -fetchone
        print(result)
        # er user og psw til í db?
        if result[0] == 1:
            cur.execute("INSERT INTO gjg_vef2vf_19v.posts VALUES(%s,%s,%s)", (pi,po,ui))
            # Commit any pending transaction to the database.
            conn.commit()
            print(result)
            cur.close()
            conn.close()
            flash('Nýr póstur hefur verið skráður í gagnagrunninn')
            return render_template('users.tpl',pi=pi)
        else:
            error = 'Nýskráning mistókst - reyndu aftur'
    return render_template('users.tpl', error=error)

@app.route('/change', methods=['GET', 'POST'])
def edit():
    if not session.get('logged_in'):
        return render_template('innskraning.tpl')
    error = None
    if request.method == 'POST':
        user = request.form.get('userID')
        try:
            cur = conn.cursor()
            result = cur.execute("SELECT * FROM gjg_vef2vf_19v.posts WHERE userID=%s",(user))       
            if  result > 0:
                userDetails = cur.fetchall()
                flash('Veldu póstnúmer')
                return render_template('change.tpl',userDetails=userDetails)
        except pymysql.IntegrityError:
            error = 'Þú hefur ekki aðgang að þessari síðu'  
        return render_template('logout.tpl')

@app.route('/changePost/<int:id>')
def editpost(id):
    try:
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='gjg', password='mypassword', database='gjg_vef2vf_19v')
        cur = conn.cursor()
        cur.execute("SELECT * FROM gjg_vef2vf_19v.posts WHERE postID=%s", id)
        conn.commit()
        result = cur.fetchall() #fáum gögnin í "tuple" 
        print(result)
        if result:
            return render_template('changePost.tpl', result=result)
        else:
            return 'Error loading #{id}'
    finally:
            cur.close()
            conn.close()

@app.route('/changed/', methods=['GET', 'POST'])
def post():
    if not session.get('logged_in'):
        return render_template('index.tpl')

    pi = request.form.get('postID')
    po = request.form.get('postur')
    ui = request.form.get('userID')
    
    button = request.form.get('breyta')
    # input VALUE = Breyta  else Eyða
    if button == 'Breyta':
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='gjg', passwd='mypassword', db='gjg_vef2vf_19v')
        cur = conn.cursor()
        cur.execute("UPDATE gjg_vef2vf_19v.posts SET postur=%s WHERE postID=%s AND userID=%s", (po, pi, ui))
        conn.commit()
        print(cur)
        cur.close()
        conn.close()
        flash('Póstinum hefur verið breytt í gagnagrunninn')
        session['logged_in'] = True
        return render_template('users.tpl')
    else:
        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='gjg', passwd='mypassword', db='gjg_vef2vf_19v')
        cur = conn.cursor()
        cur.execute("Delete FROM gjg_vef2vf_19v.posts WHERE postID=%s",(pi))
        conn.commit()
        cur.close()
        conn.close()
        flash('Póstinum hefur verið eytt úr gagnagrunninum')
        return render_template('users.tpl')

######## vefstjórn #############

@app.route('/vefstjorn')
def vefst():
    if not session.get('admin_in'):
        return render_template('vefstjori.tpl')
    else:
        return render_template('admin.tpl')

@app.route('/adminlog', methods=['GET', 'POST'])
def admlog():
    error = None
    if request.method == 'POST':
        user = request.form.get('user_name')
        psw = request.form.get('user_password')

        conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='gjg', password='mypassword', database='gjg_vef2vf_19v')
        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM gjg_vef2vf_19v.admin WHERE adminID=%s AND pass=%s",(user,psw))
        result = cur.fetchone() #fáum tuple -fetchone
        print(result)
        # er user og psw til í db?
        if result[0] == 1:
            cur.close()
            conn.close()
            flash('Ritstjórn')
            session['admin_in'] = True
            return redirect(url_for('admin'))
        else:
            error = 'Innskráning mistókst - reyndu aftur'
    return render_template('vefstjori.tpl', error=error)

@app.route('/admin')
def admin():
    if not session.get('admin_in'):
        return render_template('index.tpl')
    else:
        try:
            cur = conn.cursor()
            resultValue = cur.execute("SELECT * FROM gjg_vef2vf_19v.users")  # * = allir dálkar
            if  resultValue > 0:
                userDetails = cur.fetchall()
                flash(' vefstjóra')
                return render_template('admin.tpl',userDetails=userDetails)
        except pymysql.IntegrityError:
            error = 'Þú hefur ekki aðgang að þessari síðu'  
        return render_template('logout.tpl')

########## Útskráning ###############

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return render_template('index.tpl')

@app.route("/admin_out")
def adout():
    session['admin_in'] = False
    return render_template('index.tpl')

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.tpl'), 404

@app.errorhandler(400)
def bad_request(error):
    return render_template('bad_request.tpl'), 400

@app.errorhandler(500)
def bad_post(error):
    return render_template('bad_post.tpl'), 500

if __name__ == '__main__':
#    app.run(debug=True)
    app.run()