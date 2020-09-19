from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.review import Review

class User:

    def __init__(self, user_name: str, password: str):
        self.__user_name = user_name.lower().strip()
        self.__password = password
        self.__watched_movies = []
        self.__reviews = []
        self.__time_spent_watching_movies = 0

    @property
    def username(self):
        return self.__user_name

    @property
    def password(self):
        return self.__password

    @property
    def watched_movies(self):
        return self.__watched_movies

    @property
    def reviews(self):
        return self.__reviews

    @property
    def time_spent_watching_movies(self):
        return self.__time_spent_watching_movies

    @property
    def time_spent_watching_movies_minutes(self):
        return self.__time_spent_watching_movies

    def __repr__(self):
        return f"<User {self.__user_name}>"

    def __eq__(self, other):
        if isinstance(other, User):
            return self.__user_name == other.__user_name
        return False

    def __lt__(self, other):
        if isinstance(other, User):
            return self.__user_name < other.__user_name
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.__user_name)

    def watch_movie(self, movie: Movie):
        if movie not in self.__watched_movies:
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies += movie.runtime_minutes

    def add_review(self, review: Review):
        if review not in self.__reviews:
            self.__reviews.append(review)


