import sys
import os
import pytest
import logging


# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app import app as real_app
from models import db, User
from config import Config

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

@pytest.fixture(scope="session")
def app():
    # !Only for test usage
    real_app.config.from_object(Config)
    real_app.test_request_context().push()

    return real_app


@pytest.fixture(scope='module')
def test_client(app):
    # TODO: Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    # Insert test data
    user1 = User(name='Test User 1', email='test1@example.com')
    user2 = User(name='Test User 2', email='test2@example.com')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    yield db

    db.drop_all()
