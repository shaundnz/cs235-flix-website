from datetime import datetime

from cs235flix.domainmodel.movie import Movie


class Review:

    def __init__(self, movie: Movie, review_text: str, rating: int):
        self.__movie = movie
        self.__review_text = review_text
        if rating > 10 or rating < 1:
            self.__rating = None
        else:
            self.__rating = rating

        self.__timestamp = datetime.now()

    @property
    def movie(self):
        return self.__movie

    @property
    def review_text(self):
        return self.__review_text

    @property
    def rating(self):
        return self.__rating

    @property
    def timestamp(self):
        return self.__timestamp

    def __repr__(self):
        return f"<Movie: {self.__movie} Rating: {self.__rating} Review: {self.__review_text}>"

    def __eq__(self, other):
        if isinstance(other, Review):
            return self.movie == other.movie and self.review_text == other.review_text and self.rating == other.rating and self.timestamp == other.timestamp
        return False