from flask import Flask, request, jsonify, render_template, url_for
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_cors import CORS

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'
jwt = JWTManager(app)
CORS(app)

users = {
    "user1": {"username": "user1", "password": "password1"},
    "user2": {"username": "user2", "password": "password2"},
}

@app.route('/')
def index():
    return render_template('home.html', title='Home')

@app.route('/login', methods=['GET','POST'])
def login():
    username = request.form.get('username', None)
    password = request.form.get('password', None)
    user = users.get(username)

    if not user or user['password'] != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return jsonify(access_token=access_token, refresh_token=refresh_token)

    return render_template('login.html', title='Login')

@app.route('/shop')
def shop():
    return render_template('shop.html', title='Shop')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html', title='Attendance')

@app.route('/activity')
def activity():
    return render_template('activity.html', title='Activity')

if __name__ == '__main__':
    app.run(debug=True)
