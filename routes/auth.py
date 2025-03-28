from flask import Blueprint, request, jsonify
from app.config.db import db
from app.models.user import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    
    existing_user = User.query.filter_by(username=data.get('username')).first()
    if existing_user:
        return jsonify({'message': 'Användarnamnet är redan taget'}), 400
    
    existing_email = User.query.filter_by(email=data.get('email')).first()
    if existing_email:
        return jsonify({'message': 'E-posten är redan registrerad'}), 400
    
    
    user = User(
        username=data.get('username'),
        email=data.get('email')
    )
    user.set_password(data.get('password'))
    
    db.session.add(user)
    db.session.commit()
    
    
    access_token = create_access_token(identity=user.id)
    response_data = {
        'message': 'Användare skapad framgångsrikt',
        'access_token': access_token,
        'user': user.to_dict()
    }
    
    return jsonify(response_data), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not user.check_password(data.get('password')):
        return jsonify({'message': 'Ogiltigt användarnamn eller lösenord'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token, 'user': user.to_dict()}), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    
    if not user:
        return jsonify({'message': 'Användare hittades inte'}), 404
    
    return jsonify(user.to_dict()), 200 