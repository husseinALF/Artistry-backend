from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token
import os
from dotenv import load_dotenv


load_dotenv()

def create_app():
    app = Flask(__name__)

   
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

   
    jwt = JWTManager(app)

   
    @app.route('/')
    def home():
        return "Välkommen till ditt Flask-projekt!"


    @app.route('/login', methods=['POST'])
    def login():
        username = request.json.get("username")
        password = request.json.get("password")
        if username == "admin" and password == "password":  
            token = create_access_token(identity=username)
            return jsonify(access_token=token), 200
        return jsonify(message="Fel användarnamn eller lösenord"), 401


    @app.route('/protected', methods=['GET'])
    @jwt_required()
    def protected():
        current_user = get_jwt_identity()  
        return jsonify(logged_in_as=current_user), 200

  
    @app.route('/api/data', methods=['GET'])
    def get_data():
        data = {
            "name": "Art Gallery",
            "description": "En enkel webbsida för konstgalleri"
        }
        return jsonify(data), 200

    return app
