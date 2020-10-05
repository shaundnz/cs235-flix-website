from typing import List

from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.actor import Actor
from cs235flix.domainmodel.director import Director

class Movie:

    def __init__(self, movie_name: str, release_year: int):
        if (movie_name == "" or type(movie_name) is not str):
            self.__title = None
        else:
            self.__title = movie_name.strip()

        if release_year >= 1900:
            self.__release_year = release_year
        else:
            raise ValueError("Release year must be greater than or equal to 1900")

        self.__description = None
        self.__director = None
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = None
        self.__reviews = []

    @property
    def title(self) -> str:
        return self.__title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def description(self) -> str:
        return self.__description

    @property
    def director(self) -> Director:
        return self.__director

    @property
    def actors(self) -> List[Actor]:
        return self.__actors

    @property
    def genres(self) -> List[Genre]:
        return self.__genres

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes

    @property
    def reviews(self):
        return self.__reviews


    @title.setter
    def title(self, new_title: str):
        self.__title = new_title.strip()

    @description.setter
    def description(self, desc: str):
        self.__description = desc.strip()

    @director.setter
    def director(self, name: Director):
        self.__director = name

    @actors.setter
    def actors(self, actor_list: List[Actor]):
        self.__actors = actor_list

    @genres.setter
    def genres(self, genre_list: List[Genre]):
        self.__genres = genre_list

    @runtime_minutes.setter
    def runtime_minutes(self, time: int):
        if isinstance(time, int) and time > 0:
            self.__runtime_minutes = time
        else:
            raise ValueError

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if (isinstance(other, Movie)):
            return self.title == other.title and self.release_year == other.release_year
        return False

    def __lt__(self, other):
        if isinstance(other, Movie):
            if self.title != other.title:
                return self.title < other.title
            else:
                return self.release_year < other.release_year
        else:
            raise TypeError

    def __hash__(self):
        return hash(self.title + str(self.release_year))

    def add_actor(self, actor: Actor):
        self.__actors.append(actor)

    def remove_actor(self, actor: Actor):
        if actor in self.__actors:
            self.__actors.remove(actor)

    def add_genre(self, genre: Genre):
        self.__genres.append(genre)

    def remove_genre(self, genre):
        if genre in self.__genres:
            self.__genres.remove(genre)

    def add_review(self, review):
        self.__reviews.append(review)

    def get_reviews(self):
        return self.__reviews
