import pytest

def test_create_user(client, auth_headers):
    response = client.post('/users', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'role': 'user'
    }, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['name'] == 'Test User'
    assert data['data']['email'] == 'test@example.com'

def test_get_users(client, auth_headers):
    client.post('/users', json={'name': 'User1', 'email': 'user1@example.com', 'role': 'user'}, headers=auth_headers)
    client.post('/users', json={'name': 'User2', 'email': 'user2@example.com', 'role': 'user'}, headers=auth_headers)
    
    response = client.get('/users', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 3

def test_get_user_by_id(client, auth_headers):
    create_resp = client.post('/users', json={'name': 'User1', 'email': 'user1@example.com', 'role': 'user'}, headers=auth_headers)
    user_id = create_resp.get_json()['data']['id']
    
    response = client.get(f'/users/{user_id}', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['data']['id'] == user_id

def test_search_users(client, auth_headers):
    client.post('/users', json={'name': 'Alice Smith', 'email': 'alice@example.com', 'role': 'user'}, headers=auth_headers)
    client.post('/users', json={'name': 'Bob Jones', 'email': 'bob@example.com', 'role': 'user'}, headers=auth_headers)
    
    response = client.get('/users?search=alice', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 1
    assert data['data'][0]['name'] == 'Alice Smith'

def test_pagination(client, auth_headers):
    for i in range(15):
        client.post('/users', json={'name': f'User {i}', 'email': f'user{i}@example.com', 'role': 'user'}, headers=auth_headers)
    
    response = client.get('/users?page=2&limit=10', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) == 6
    assert data['page'] == 2
    assert data['total'] == 16

def test_duplicate_email(client, auth_headers):
    client.post('/users', json={'name': 'User1', 'email': 'duplicate@example.com', 'role': 'user'}, headers=auth_headers)
    
    response = client.post('/users', json={'name': 'User2', 'email': 'duplicate@example.com', 'role': 'user'}, headers=auth_headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert "already registered" in data['error'].lower()

def test_missing_fields(client, auth_headers):
    response = client.post('/users', json={'name': 'User1'}, headers=auth_headers)
    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] is False
    assert "required" in data['error'].lower()

def test_user_not_found(client, auth_headers):
    response = client.get('/users/999', headers=auth_headers)
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert data['error'] == "User not found"
