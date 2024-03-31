from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os

app = Flask(__name__)
app.secret_key = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = '1775c315bb6aeee24e3be1f335f6fceaaafc4d55e4f50419'
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)
jwt = JWTManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(80))
    profile_picture = db.Column(db.String(100))

class Invitation(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone_number = db.Column(db.String(20))
    alternate_email = db.Column(db.String(100), nullable=True)
    organizations = db.relationship('Organization', backref='invitation', lazy=True)

class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    valid_till = db.Column(db.Date)
    invitation_id = db.Column(db.String(36), db.ForeignKey('invitation.id'))

with app.app_context():
    db.create_all()

@app.route('/signup', methods=['POST'])
def signup():
    invitation_id = request.json.get('invitation_id')
    invitation = Invitation.query.filter_by(id=invitation_id).first()
    if not invitation:
        return jsonify({'message': 'Invalid invitation ID'}), 400
    hashed_password = generate_password_hash(request.json['password'], method='pbkdf2:sha256')
    new_user = User(username=invitation.name, email=invitation.email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=email)
        user_details = {'username': user.username, 'email': user.email, 'profile_picture': user.profile_picture}
        return jsonify(access_token=access_token, user_details=user_details)
    else:
        return jsonify({'message': 'Login attempt failed'}), 401

@app.route('/logout')
def logout():
    return jsonify({'message': 'Logged out successfully'})

@app.route('/invite', methods=['POST'])
@jwt_required()
def invite():
    current_user = get_jwt_identity()
    invitation_data = request.json
    invitation_id = str(uuid.uuid4())
    invitation = Invitation(
        id=invitation_id,
        name=invitation_data['name'],
        email=invitation_data['email'],
        phone_number=invitation_data['phone_number'],
        alternate_email=invitation_data.get('alternate_email')
    )
    organizations_data = invitation_data.get('organizations', [])
    for org_data in organizations_data:
        valid_till_date = datetime.strptime(org_data['valid_till'], '%Y-%m-%d').date() if 'valid_till' in org_data else None
        organization = Organization(
            name=org_data['name'],
            role=org_data['role'],
            valid_till=valid_till_date,
            invitation_id=invitation_id
        )
        db.session.add(organization)
    db.session.add(invitation)
    db.session.commit()
    return jsonify({'message': 'Invitation sent successfully', 'invitation_id': invitation_id})

@app.route('/edit_user', methods=['PUT'])
@jwt_required()
def edit_user():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = request.json
    user.username = user_data.get('username', user.username)
    user.email = user_data.get('email', user.email)
    db.session.commit()
    return jsonify({'message': 'User details updated successfully'})

@app.route('/upload_profile_picture', methods=['POST'])
@jwt_required()
def upload_profile_picture():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        user.profile_picture = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        db.session.commit()
        return jsonify({'message': 'Profile picture uploaded successfully'})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)
