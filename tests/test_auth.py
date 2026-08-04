def test_register_user(client):
    response = client.post('/auth/register', json={
        'name': 'Auth User',
        'email': 'auth@example.com',
        'password': 'password123',
        'role': 'user'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['email'] == 'auth@example.com'
    assert 'password_hash' not in data['data']

def test_register_duplicate(client):
    client.post('/auth/register', json={
        'name': 'Auth User',
        'email': 'auth@example.com',
        'password': 'password123',
        'role': 'user'
    })
    response = client.post('/auth/register', json={
        'name': 'Auth User2',
        'email': 'auth@example.com',
        'password': 'password123',
        'role': 'user'
    })
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False

def test_login_success(client):
    client.post('/auth/register', json={
        'name': 'Auth User',
        'email': 'auth@example.com',
        'password': 'password123',
        'role': 'user'
    })
    response = client.post('/auth/login', json={
        'email': 'auth@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'token' in data['data']
    assert data['data']['user']['email'] == 'auth@example.com'

def test_login_invalid(client):
    client.post('/auth/register', json={
        'name': 'Auth User',
        'email': 'auth@example.com',
        'password': 'password123',
        'role': 'user'
    })
    response = client.post('/auth/login', json={
        'email': 'auth@example.com',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data['success'] is False

def test_protected_routes(client):
    response = client.get('/users')
    assert response.status_code == 401
