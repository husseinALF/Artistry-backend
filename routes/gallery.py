from flask import Blueprint, request, jsonify, current_app
from app.config.db import db
from app.models.artwork import Artwork
from app.models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
from werkzeug.utils import secure_filename
import uuid

gallery_bp = Blueprint('gallery', __name__)

def save_image(file):
    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
    
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder, mode=0o755, exist_ok=True)
    
    filename = secure_filename(file.filename)
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    if file_ext not in allowed_extensions:
        raise ValueError(f"Endast {', '.join(allowed_extensions)} är tillåtna filtyper")
    
    random_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(upload_folder, random_filename)
    file.save(file_path)
    
    return f"/static/uploads/{random_filename}"

@gallery_bp.route('/', methods=['GET'])
def get_all_artworks():
    artworks = Artwork.query.all()
    return jsonify([artwork.to_dict() for artwork in artworks]), 200

@gallery_bp.route('/', methods=['POST'])
@jwt_required()
def create_artwork():
    try:
        current_user_id = get_jwt_identity()
        
        try:
            current_user_id = int(current_user_id)
        except:
            return jsonify({'message': 'Ogiltigt användar-ID'}), 400
        
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'message': 'Användare hittades inte'}), 404
        
        if 'image' not in request.files:
            return jsonify({'message': 'Ingen bild har skickats'}), 400
        
        file = request.files['image']
        if file.filename == '':
            return jsonify({'message': 'Ingen bild har valts'}), 400
        
        file_content = file.read()
        file_size = len(file_content)
        
        if file_size > 10 * 1024 * 1024: 
            return jsonify({'message': 'Filen är för stor. Max 10 MB tillåtet.'}), 413
        
        file.seek(0)
            
        try:
            image_path = save_image(file)
        except ValueError as e:
            return jsonify({'message': str(e)}), 422
        except Exception as e:
            return jsonify({'message': f'Kunde inte spara bilden: {str(e)}'}), 500
        
        artwork = Artwork(
            title=request.form.get('title'),
            description=request.form.get('description', ''),
            image_path=image_path,
            user_id=current_user_id
        )
        
        db.session.add(artwork)
        db.session.commit()
        
        return jsonify(artwork.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Ett fel uppstod: {str(e)}'}), 500