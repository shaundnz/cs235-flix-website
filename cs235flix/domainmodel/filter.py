import csv
from collections import OrderedDict

from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.actor import Actor
from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.director import Director


class Filter:

    def __init__(self, data_filename):
        self.__filename = data_filename

    def contains_title(self, title, row):
        if title == "*":
            return True
        return title in row["Title"]

    def contains_actor(self, actor, row):
        if actor == "*":
            return True
        return actor in row["Actors"]

    def contains_genre(self, genre, row):
        if genre == "*":
            return True
        return genre in row["Genre"]

    def contains_director(self, director, row):
        if director == "*":
            return True
        return director in row["Director"]

    def create_movie_instance(self, row):
        movie = Movie(row["Title"], int(row["Year"]))
        movie.director = Director(row["Director"])
        movie.runtime_minutes = int(row["Runtime (Minutes)"])
        movie.actors = [Actor(actor.strip()) for actor in row['Actors'].split(",")]
        movie.genres = [Genre(genre.strip()) for genre in row['Genre'].split(",")]
        movie.description = row["Description"]
        return movie

    def filter_movies(self, title="*", genre="*", actor="*", director="*"):
        result_set = []
        with open(self.__filename, mode='r', encoding='utf-8-sig') as csvfile:
            movie_file_reader = csv.DictReader(csvfile)

            for row in movie_file_reader:
                if self.contains_title(title, row) and \
                        self.contains_actor(actor, row) and \
                        self.contains_genre(genre, row) and \
                        self.contains_director(director, row):
                    result_set.append(self.create_movie_instance(row))

        return result_set
