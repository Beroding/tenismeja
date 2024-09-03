from flask import Flask, request, jsonify, render_template, redirect, url_for, flash, session
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
app.secret_key = 'another-secret-key'
jwt = JWTManager(app)
CORS(app)

users = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"},
}

def load_users():
    with open('data/users.json') as f:
        return json.load(f)

def save_attendance(username, note):
    with open(f'data/{username}_attendance.json', 'a') as f:
        attendance = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "note": note
        }
        f.write(json.dumps(attendance) + '\n')

@app.route('/')
def index():
    return render_template('home.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        user = users.get(username)

        if not user or user['password'] != password:
            flash("Wrong Username or Password", "danger")
            return redirect(url_for('login'))

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        
        session['username'] = username
        flash("Logged in successfully!", "success")
        return redirect(url_for('attendance'))
    
    return render_template('login.html', title='Login')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged out successfully!", "success")
    return redirect(url_for('login'))

@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    # if request.method == 'POST':
    #     fullname = request.form.get('fullname', None)
    #     kelas = request.form.get('kelass', None)
    # save_attendance(session['username'], note)
    
    return render_template('attendance.html', title='Attendance')

@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop')

@app.route('/activity')
def activity():
    return render_template('activity.html', title='Activity')

if __name__ == '__main__':
    app.run(debug=True)
