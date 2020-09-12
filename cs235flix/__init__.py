"""Initialize CS235-Flix Flask app."""

import os

from flask import Flask

import cs235flix.adapters.repository as repo
from cs235flix.adapters.memory_repository import MemoryRepository, populate


def create_app(test_config=None):
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
    repo.repo_instance = MemoryRepository()

    # Populate the MemoryRepository with data
    populate(data_path, repo.repo_instance)

    # TODO Build the application
    with app.app_context():
        # Register blueprints
        from .movies import movies
        app.register_blueprint(movies.movies_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

    return app