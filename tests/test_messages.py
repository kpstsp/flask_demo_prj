from models import User, Message



def test_create_message(test_client, init_database):
    user = User.query.filter_by(email='test1@example.com').first()
    response = test_client.post('/messages', json={
        'sender_id': user.id,
        'content': 'Hello, Friend!'
    })

    assert response.status_code == 201
    data = response.get_json()
    assert data['message_data']['content'] == 'Hello, Friend!'
    

def test_get_messages_by_user(test_client, init_database):
    user = User.query.filter_by(email='test1@example.com').first()
    response = test_client.get('/messages', query_string={'user_id': user.id})

    assert response.status_code == 200
    data = response.get_json()
    assert len(data['messages']) == 1
    assert data['messages'][0]['content'] == 'Hello, Friend!'
