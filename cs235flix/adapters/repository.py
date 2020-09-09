import abc

from cs235flix.domainmodel.actor import Actor
from cs235flix.domainmodel.director import Director
from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.user import User
from cs235flix.domainmodel.movie import Movie

repo_instance = None

class AbstractRepository(abc.ABC):

    # Add movie to the repository
    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        raise NotImplementedError

    # Get a movie from the repository by its ID (rank)
    @abc.abstractmethod
    def get_movie(self, movie_name: str, release_year: int) -> Movie:
        raise NotImplementedError

    # Add an actor to the repository
    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        raise NotImplementedError

    # Get an actor from the repo by name
    @abc.abstractmethod
    def get_actor(self, actor_name: str) -> Actor:
        raise NotImplementedError

    # Add an genre to the repository
    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        raise NotImplementedError

    # Get an genre by name
    @abc.abstractmethod
    def get_genre(self, genre_name: str) -> Genre:
        raise NotImplementedError

    # Add a director to the repo
    @abc.abstractmethod
    def add_director(self, director: Director):
        raise NotImplementedError

    # Get a director by name
    @abc.abstractmethod
    def get_director(self, director_name: str) -> Director:
        raise NotImplementedError

