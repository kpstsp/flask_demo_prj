from flask import Flask, request, jsonify
from models import db, User, Message
from __init__ import create_app

app = create_app()

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def add_user():
    print("Debug: Received request to /users")  # Print debug info
    
    data = request.json
    print(f"Debug: Request data: {data}")  # Print request data
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    print(f"Debug: Created user: {new_user}")  # Print created user info
    return jsonify({"message": "User added successfully!", "user": {"id": new_user.id, "name": new_user.name, "email": new_user.email}}), 201

# Endpoint to delete a user by ID
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully!"}), 200

# Endpoint to update a user's details by ID
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()
    return jsonify({"message": "User updated successfully!", "user": {"id": user.id, "name": user.name, "email": user.email}}), 200

# Endpoint to fetch a user by their email
@app.route('/users', methods=['GET'])
def get_user_by_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    return jsonify({"user": {"id": user.id, "name": user.name, "email": user.email}}), 200

# Endpoint to create a new message
@app.route('/messages', methods=['POST'])
def send_message():
    data = request.json
    print(f"Debug: Data: {data}")  # Print debug info
    user = User.query.filter_by(id=data['sender_id']).first()
    print(f"Debug: User: {user}")  # Print debug info
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    new_message = Message(sender=user, content=data['content'])
    db.session.add(new_message)
    db.session.commit()
    return jsonify({"message": "Message sent successfully!", "message_data": {"id": new_message.id, "sender": user.name, "content": new_message.content, "timestamp": new_message.timestamp}}), 201

# Endpoint to delete a message by ID
@app.route('/messages/<int:message_id>', methods=['DELETE'])
def delete_message(message_id):
    message = Message.query.get(message_id)
    if not message:
        return jsonify({"message": "Message not found!"}), 404
    db.session.delete(message)
    db.session.commit()
    return jsonify({"message": "Message deleted successfully!"}), 200

# Endpoint to fetch all messages sent by a given user
@app.route('/messages', methods=['GET'])
def get_messages_by_user():
    user_id = request.args.get('user_id')
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found!"}), 404
    
    messages = Message.query.filter_by(sender_id=user_id).all()
    result = []
    for message in messages:
        result.append({
            "id": message.id,
            "content": message.content,
            "timestamp": message.timestamp
        })
    return jsonify({"messages": result}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
