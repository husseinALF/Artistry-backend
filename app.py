from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app, 
         resources={r"/*": {
             "origins": ["http://localhost:5173"],  
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "allow_credentials": True  
         }})
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
    
    app.config['JWT_ERROR_MESSAGE_KEY'] = 'message'
    
    jwt = JWTManager(app)
    

    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return str(user)
    
    from routes.auth import auth_bp
    from routes.gallery import gallery_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(gallery_bp, url_prefix='/api/gallery')
    
    return app