import abc

from cs235flix.domainmodel.user import User
from cs235flix.domainmodel.movie import Movie

repo_instance = None

class AbstractRepository(abc.ABC):

    # Add user to the repository
    @abc.abstractmethod
    def add_user(self, user: User):
        raise NotImplementedError

    # Get a user from the repository
    @abc.abstractmethod
    def get_user(self, username) -> User:
        raise NotImplementedError

    # Add movie to the repository
    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        raise NotImplementedError

    # Get a movie from the repository by its ID (rank)
    @abc.abstractmethod
    def get_movie(self, id):
        raise NotImplementedError

