import pytest
from app import app, db, User
from flask_jwt_extended import create_access_token

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/register', json={
        'full_name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert response.get_json()['message'] == 'User registered successfully'

def test_login(client):
    client.post('/register', json={
        'full_name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    response = client.post('/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert 'access_token' in response.get_json()

def test_profile(client):
    client.post('/register', json={
        'full_name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    access_token = create_access_token(identity='test@example.com')
    headers = {'Authorization': f'Bearer {access_token}'}
    response = client.get('/profile', headers=headers)
    assert response.status_code == 200
    assert response.get_json()['email'] == 'test@example.com'
