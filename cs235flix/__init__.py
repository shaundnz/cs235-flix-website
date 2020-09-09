"""Initialize CS235-Flix Flask app."""

import os

from flask import Flask

def create_app(test_config = None):
    app = Flask(__name__)

    # Set up config file
    app.config.from_object('config.Config')

    # Config data path for the repository
    data_path = os.path.join('cs235flix', 'adapters', 'data')

    # TODO Load the test configuration, override any config settings
    if test_config is not None:
        #app.config.from_mapping(test_config)
        #data_path = app.config['TEST_DATA_PATH']
        pass


    # TODO Set up memory repository
    # repo = MemoryRepository()

    # Populate the MemoryRepository with data
    # populate(data_path, repo.repo_instance)

    # TODO Build the application
    with app.app_context():
        # Register blueprints
        pass


