import pytest
from app import create_app
from app.config import TestingConfig
from app.extensions import db

@pytest.fixture
def app():
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    client.post('/auth/register', json={
        'name': 'Test Auth User',
        'email': 'auth_client@example.com',
        'password': 'password123',
        'role': 'user'
    })
    resp = client.post('/auth/login', json={
        'email': 'auth_client@example.com',
        'password': 'password123'
    })
    token = resp.get_json()['data']['token']
    return {'Authorization': f'Bearer {token}'}
