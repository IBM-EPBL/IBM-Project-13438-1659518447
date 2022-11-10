from flask import Flask, render_template, request,redirect,session, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import mysql.connector
import os
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key=os.urandom(24)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'digit_recognition'

mysql = MySQL(app)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register/')
def about():
    return render_template('form.html')

@app.route('/home')
def home():
    if 'email' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation',methods=['POST'])
def login_validation():
    email=request.form.get('email')
    password=request.form.get('password')
    if mysql:
        print("Connection Successful!")
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT * FROM `users` where `Email` LIKE '{}' and `Password` LIKE '{}'""".format(email, password))
        users = cursor.fetchall()
        cursor.close()
    else:
        print("Connection Failed!")

    if len(users)>0:
        session['email'] = users[0][1]
        return redirect('/home')
    else:
        return redirect('/')
    

@app.route('/add_user',methods=['POST'])
def add_user():
    username=request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    phone = request.form.get('phone')
    gender = request.form.get('gender')
    if mysql:
        print("Connection Successful!")
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO `users` (`FullName`,`Email`,`Password`,`PhoneNo`,`Gender`) VALUES ('{}','{}','{}','{}','{}')""".format(username,email, password,phone,gender))
        mysql.connection.commit()
        cursor.close()
    else:
        print("Connection Failed!")
    return "User Registered Successfully."


@app.route('/logout')
def logout():
    session.pop('email')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

