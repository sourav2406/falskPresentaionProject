import os
import sqlite3
from flask import Flask, render_template, request, session, g, redirect, url_for, abort, flash
from flaskext.mysql import MySQL

 # create our little application :)
app = Flask(__name__)
mysql = MySQL()
app.config.from_object(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root123'
app.config['MYSQL_DATABASE_DB'] = 'userData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

# Load default config and override config from an environment variable
app.config.update(dict(
    #DATABASE=os.path.join(app.root_path, 'mainApp.db'),
    SECRET_KEY='development_key',
    USERNAME='admin',
    PASSWORD='123456'
))

# def connect_db():
#     """Connects to the specific database."""
#     rv = sqlite3.connect(app.config['DATABASE'])
#     rv.row_factory = sqlite3.Row
#     return rv
# 
# def get_db():
#     """Opens a new database connection if there is none yet for the
#     current application context.
#     """
#     if not hasattr(g, 'sqlite_db'):
#         g.sqlite_db = connect_db()
#     return g.sqlite_db
# 
# def init_db():
#     db = get_db()
#     with app.open_resource('schema.sql', mode='r') as f:
#         db.cursor().executescript(f.read())
#     db.commit()
#     
# @app.cli.command('initdb')
# def initdb_command():
#     """Initializes the database."""
#     init_db()
#     print 'Initialized the database.'
#     
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     if hasattr(g, 'sqlite_db'):
#         g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    error = None
    if session.get('logged_in'):
        return render_template('index.html')
    
    if request.method == 'POST':
#         db = get_db()
#         cur = db.execute('select name from user_info where name="'+request.form['username']+'" and password="'
#                          +request.form['password']+'"')
#         entries = cur.fetchall()
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connect().cursor()
        cursor.execute("SELECT * from user_info where name='" + username + "' and password='" + password + "'")
        data = cursor.fetchone()
        #if not entries:
        if data is None:
            error = "Invalid Username or password!"
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('index'))
    return render_template('login.html',error=error)

@app.route('/logout/')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


@app.route('/register/', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        error = validate(request.form);
        if error is None :
#             db = get_db()
#             db.execute('insert into user_info (name, password, email, phone) values (?, ?, ?, ?)',
#                  [request.form['username'], request.form['password'], request.form['email'], request.form['phone']])
#             db.commit()
            flash('New user registration successfully completed!!')
            return redirect(url_for('login'))
        
    return render_template('register.html',error=error)

def validate(data):
    if not data['username']:
        return "Username Should not be blank"
    elif not data['password']:
        return "Password Should not be blank"