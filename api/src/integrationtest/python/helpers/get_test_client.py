import os
from flask.ctx import AppContext
from database_api import app
from flask.testing import FlaskClient

def get_test_client() -> (AppContext, FlaskClient):
    os.environ["CONFIG_TYPE"] = "config.TestingConfig"
    with app.test_client() as testing_client:
        with app.app_context() as app_context:
            return (app_context, testing_client)