from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '#'
app.config['MYSQL_DB'] = 'login'

mysql = MySQL(app)

@app.route("/", methods=["GET"])
def home():
    return render_template("about.html")
@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE username = % s AND password = % s', (username, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['userid'] = account['userid']
			session['username'] = account['username']
			msg = 'Logged in successfully !'
			return render_template('index.html', msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('userid', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM users WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)

@app.route('/create_greenhouse', methods=['GET', 'POST'])
def create_greenhouse():
    msg = ''
    if request.method == 'POST' and 'location' in request.form and 'greenhouse_name' in request.form and 'sensors' in request.form and 'length' in request.form and 'width' in request.form:
        location = request.form['location']
        greenhouse_name = request.form['greenhouse_name']
        sensors = request.form['sensors']
        length = request.form['length']
        width = request.form['width']
        username = session['username'] # retrieve username from session
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT userid FROM users WHERE username = %s', (username,))
        userid = cursor.fetchone()[0]
        cursor.execute('INSERT INTO greenhouses (location, greenhouse_name, sensors, length, width, userid) VALUES (%s, %s, %s, %s, %s, %s)', (location, greenhouse_name, sensors, length, width, userid))
        mysql.connection.commit()
        msg = 'You have successfully created a new greenhouse!'
    return render_template('details.html', msg=msg)

@app.route('/existing_greenhouse')
def existing():
	return render_template('existing.html')
	
@app.route('/sensor_status')
def sensor_status():
    msg = ''
    # Query sensor_status table
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM sensor_status")
    rows = cursor.fetchall()
    # Pass data to HTML template
    return render_template('sensor_status.html', rows=rows, msg=msg)

if __name__ == '__main':
	app.run(debug=True)