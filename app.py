from flask import Flask, request, jsonify
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

USERS_FILE = 'users.txt'
TOTAL_FILE = 'total_users.txt'
EMAIL_ADDRESS = 'master_key_sricpt@proton.me'
EMAIL_PASSWORD = '2K%3a>)~ukwnT*>'
TO_EMAIL = 'edmilsonander83@gmail.com'

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form.get('username')
    if not username:
        return jsonify({'error': 'No username provided'}), 400

    if not os.path.exists(USERS_FILE):
        open(USERS_FILE, 'w').close()

    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()

    if username not in users:
        with open(USERS_FILE, 'a') as f:
            f.write(username + '\n')

    total_users = len(users) + 1  # Consider the new user added
    with open(TOTAL_FILE, 'w') as f:
        f.write(str(total_users))

    send_email('User Registration', f'New user registered: {username}\nTotal users: {total_users}')
    
    return jsonify({'message': 'User registered successfully'}), 200

@app.route('/stats', methods=['GET'])
def get_stats():
    if not os.path.exists(USERS_FILE):
        return jsonify({'total_users': 0, 'users': []})

    with open(USERS_FILE, 'r') as f:
        users = f.read().splitlines()

    total_users = len(users)
    return jsonify({'total_users': total_users, 'users': users})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
