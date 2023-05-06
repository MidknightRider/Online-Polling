from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
import os
from twilio.rest import Client
import uuid

app = Flask(__name__)
db = sqlite3.connect('users.db', check_same_thread=False)
app.secret_key = os.urandom(16)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get user data from the registration form
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']

        # Generate a unique user ID
        user_id = str(uuid.uuid4())

        # Insert user data into the database
        cursor = db.cursor()

        cursor.execute(
            'SELECT * FROM users WHERE email = ? OR phone = ?', (email, phone))
        existing_user = cursor.fetchone()

        if existing_user:
            return "User already exists!"

        else:
            cursor.execute('INSERT INTO users (id, name, email, phone, password) VALUES (?, ?, ?, ?, ?)',
                           (user_id, name, email, phone, password))
            db.commit()
            cursor.close()
            # Redirect to the login page
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        phone = request.form['phone']
        password = request.form['password']

        # Generate a unique user ID
        user_id = str(uuid.uuid4())

        # Set session ID to unique user ID
        session["user"] = user_id
        
        cursor = db.cursor()
        cursor.execute('SELECT * FROM users WHERE phone = ?', (phone,))
        user = cursor.fetchone()

        if user:
            if user[4] == password:
                return render_template('OTP.html')
            else:
                print('Failed to log in...')
                redirect(url_for(login))

    return render_template('login.html')


@app.route('/login/OTP')
def OTP():
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Hello, there!',
        to='whatsapp:+15005550006'
    )


if __name__ == '__main__':
    app.run()
