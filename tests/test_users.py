from models import User



def test_create_user(test_client):
    # print("Debug: Starting test_create_user")  # Debug print
    response = test_client.post('/users', json={
        'name': 'TestUser3',
        'email': 'test3@example.com'
    })

    # print(f"Debug: Response status code: {response.status_code}")  # Debug print
    assert response.status_code == 201
    data = response.get_json()
    # print(f"Debug: Response data: {data}")  # Debug print
    assert data['user']['name'] == 'TestUser3'
    assert data['user']['email'] == 'test3@example.com'

def test_get_user_by_email(test_client, init_database):
    response = test_client.get('/users', query_string={'email': 'test3@example.com'})

    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['name'] == 'TestUser3'
    assert data['user']['email'] == 'test3@example.com'

def test_update_user(test_client, init_database):
    user = User.query.filter_by(email='test3@example.com').first()
    response = test_client.put(f'/users/{user.id}', json={
        'name': 'Updated User 3',
        'email': 'updated1@example.com'
    })

    assert response.status_code == 200
    data = response.get_json()
    assert data['user']['name'] == 'Updated User 3'
    assert data['user']['email'] == 'updated1@example.com'

def test_delete_user(test_client, init_database):
    user = User.query.filter_by(email='test2@example.com').first()
    response = test_client.delete(f'/users/{user.id}')

    assert response.status_code == 200
