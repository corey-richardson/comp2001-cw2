from flask import request, jsonify
from config import app, db
from models import User

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(email=data['email'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'email': user.email, 'role': user.role} for user in users])