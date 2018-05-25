from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import secrets

#

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

#

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    admin = db.Column(db.Boolean)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

#

@app.route('/')
def index():
    return 'Check out this API!'

@app.route('/users', methods=['GET'])
def get_all_users():
    '''
    Return all users
    '''
    users = User.query.order_by(User.join_date.desc()).all()

    users_list = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['admin'] = user.admin
        user_data['join_date'] = user.join_date
        users_list.append(user_data)

    return jsonify({'users': users_list})

@app.route('/user/new', methods=['POST'])
def create_user():
    '''
    Create a new user
    '''
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data['password'])
    new_user = User(public_id=str(secrets.token_hex(10)),
                    username=data['username'],
                    email=data['email'],
                    password=hashed_password,
                    admin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created'})

@app.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    '''
    Return a single user with public_id <id>
    '''
    user = User.query.filter_by(public_id=id).first()
    return jsonify({'user': {'public_id': user.public_id, 'name': user.username}})

@app.route('/user/promote/<string:id>', methods=['PUT'])
def promote_user(id):
    '''
    Give user with public_id <id> admin status
    '''
    user = User.query.filter_by(public_id=id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    if user.admin:
        return jsonify({'message': 'User already has admin status!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message': f'User ({id}) promoted!'})

@app.route('/user/demote/<string:id>', methods=['PUT'])
def demote_user(id):
    '''
    Remove admin status from user with public_id <id>
    '''
    user = User.query.filter_by(public_id=id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    if not user.admin:
        return jsonify({'message': 'User is not an admin!'})

    user.admin = False
    db.session.commit()

    return jsonify({'message': f'User ({id}) demoted!'})

@app.route('/user/delete/<string:id>', methods=['DELETE'])
def delete_user(id):
    '''
    Delete user with public_id <id>
    '''
    user = User.query.filter_by(public_id=id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': f'User ({id}) deleted!'})

#
#
#

if __name__ == '__main__':
    app.run(debug=True)
