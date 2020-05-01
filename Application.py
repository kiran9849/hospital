from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re



app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'database-1.cto4v9ebtabk.us-west-2.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'Kiran123'
app.config['MYSQL_DB'] = 'pythonlogin'


mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - this will be the login page, we need to use both GET and POST requests

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('opform'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)



@app.route('/add_data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        firstname = request.form['fname']
        place = request.form['place']
        lastname = request.form['lname']
        startdate = request.form['sdate']
        duedate = request.form['ddate']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('''INSERT INTO opform (firstname, place, lastname, startdate, duedate) VALUES (%s, %s, %s, %s, %s)''', (firstname, place, lastname, startdate, duedate))
        mysql.connection.commit()
        return redirect(url_for('opform'))
    else:
        return render_template('opform.html')

@app.route('/opform', methods=['GET', 'POST'])
def opform():
    add_data()
    return render_template('opform.html')


@app.route('/')
@app.route('/')
def example():
    conn = MySQLdb.connect("database-1.cto4v9ebtabk.us-west-2.rds.amazonaws.com", "admin", "Kiran123", "pythonlogin")
    cursor = conn.cursor()
    #cursor.execute("select * from opform where duedate between adddate(now(),+7) and now()")
    #cursor.execute("select * from opform where duedate >= curdate() - INTERVAL DAYOFWEEK(curdate())+6 DAY AND duedate < curdate() - INTERVAL DAYOFWEEK(curdate())-1 DAY")
    cursor.execute("select * from opform where duedate =CURDATE() or DATEDIFF(duedate, DATE_ADD(CURDATE(), INTERVAL 1 DAY)) = 0 or DATEDIFF(duedate, DATE_ADD(CURDATE(), INTERVAL 2 DAY)) = 0 or DATEDIFF(duedate, DATE_ADD(CURDATE(), INTERVAL 3 DAY)) = 0")
    data = cursor.fetchall() #data from database
    return render_template("index.html", value=data)



# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)