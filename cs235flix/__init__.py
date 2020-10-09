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

    repo.repo_instance = MemoryRepository()

    if test_config is not None:
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
        populate(os.path.join(data_path), "Data100movies.csv", repo.repo_instance)
    else:
        populate(os.path.join(data_path), "Data1000movies.csv", repo.repo_instance)



    # repo.repo_instance = MemoryRepository()

    # Populate the MemoryRepository with data
    #populate(os.path.join(data_path), "Data1000movies.csv", repo.repo_instance)


    with app.app_context():
        # Register blueprints
        from .movies import movies
        app.register_blueprint(movies.movies_blueprint)

        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .genres import genres
        app.register_blueprint(genres.genres_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

    return app