from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os
import secrets


# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/userdb')
app.config['JWT_SECRET_KEY'] = secrets.token_hex(64)

db = SQLAlchemy(app)
jwt = JWTManager(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

def create_user(full_name, email, password):
    hashed_password = generate_password_hash(password)
    new_user = User(full_name=full_name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    create_user(data['full_name'], data['email'], data['password'])
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.email)
        return jsonify(access_token=access_token)
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    user = User.query.filter_by(email=current_user).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify(full_name=user.full_name, email=user.email)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'message': 'Resource not found. Please use /api/docs for documentation.'
        }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'message': 'Internal server error'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'message': 'Bad request'}), 400

@app.errorhandler(401)
def unauthorized(error):
    return jsonify({'message': 'Unauthorized'}), 401

@app.errorhandler(403)
def forbidden(error):
    return jsonify({'message': 'Forbidden'}), 403

@app.errorhandler(409)
def conflict(error):
    return jsonify({'message': 'Conflict'}), 409

@app.errorhandler(422)
def unprocessable_entity(error):
    return jsonify({'message': 'Unprocessable entity'}), 422

# Swagger documentation setup
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': 'User Management API'})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
