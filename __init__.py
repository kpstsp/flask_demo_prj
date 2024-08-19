from flask import Flask
from config import Config 
from models import db, User

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.debug = True
    db.init_app(app)

    with app.app_context():
        db.create_all()

        if not User.query.first():
            populate_test_data()    

    return app

def populate_test_data():
    """Function to populate the database with test data."""
    test_users = [
        User(name='Alice', email='alice@example.com'),
        User(name='Bob', email='bob@example.com'),
        User(name='Charlie', email='charlie@example.com')
    ]
    db.session.bulk_save_objects(test_users)
    db.session.commit()
    print("Test users added to the database.")
