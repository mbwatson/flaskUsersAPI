from datetime import datetime, timedelta
from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import jwt
import secrets
#

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secrets'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Models

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    first_name = db.Column(db.String(20), unique=False, nullable=True)
    last_name = db.Column(db.String(20), unique=False, nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean, nullable=False, default=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    join_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

# Routes

@app.route('/')
def index():
    return 'The API is ready!'

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Username and password are required!'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return jsonify({'message': 'Invalid login information!'})

    if bcrypt.check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=10)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})
    else:
        return jsonify({'message': 'Invalid login information!'})

    return jsonify({'message': 'Something went wrong!'})

@app.route('/users', methods=['GET'])
def get_all_users():
    '''
    Return all users as JSON
    '''
    users = User.query.order_by(User.join_date.desc()).all()

    users_list = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['username'] = user.username
        user_data['email'] = user.email
        user_data['admin'] = user.admin
        user_data['active'] = user.active
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
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    username=data['username'],
                    email=data['email'],
                    password=hashed_password,
                )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'new user created'})

@app.route('/user/<string:id>', methods=['GET'])
def get_user(id):
    '''
    Return a single user with public_id <id> as JSON
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

@app.route('/user/deactivate/<string:id>', methods=['PUT'])
def deactivate_user(id):
    '''
    Deactivate user with public_id <id>
    '''
    user = User.query.filter_by(public_id=id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    if not user.active:
        return jsonify({'message': 'User is already deactivated!'})

    user.active = False
    db.session.commit()

    return jsonify({'message': f'User ({id}) deactivated!'})

@app.route('/user/activate/<string:id>', methods=['PUT'])
def activate_user(id):
    '''
    Activate user with public_id <id>
    '''
    user = User.query.filter_by(public_id=id).first()

    if not user:
        return jsonify({'message': 'User not found!'})

    if user.active:
        return jsonify({'message': 'User is already active!'})

    user.active = True
    db.session.commit()

    return jsonify({'message': f'User ({id}) activated!'})

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
