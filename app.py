from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

# Ladda miljövariabler
load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Konfiguration från miljövariabler
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    
    # Initiera JWT
    JWTManager(app)
    
    return app
