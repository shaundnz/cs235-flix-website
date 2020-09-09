import os
from typing import List
import csv

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.actor import Actor
from cs235flix.domainmodel.director import Director
from cs235flix.domainmodel.movie import Movie

class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__movies = list()
        self.__movies_dict = dict()

        self.__genre = list()
        self.__genre_dict = dict()

        self.__actors = list()
        self.__actors_dict = dict()

        self.__directors = list()
        self.__directors_dict = dict()

        self.__users = list()

    def add_movie(self, movie: Movie):
        self.__movies.append(movie)
        self.__movies_dict[movie] = movie

    def get_movie(self, movie_name, release_year) -> Movie:
        movie = None
        try:
            movie = self.__movies_dict[Movie(movie_name, release_year)]
        except KeyError:
            pass
        return movie

    def add_actor(self, actor: Actor):
        if actor not in self.__actors:
            self.__actors.append(actor)
            self.__actors_dict[actor] = actor

    def get_actor(self, actor_name: str) -> Actor:
        actor = None
        try:
            actor = self.__actors_dict[Actor(actor_name)]
        except KeyError:
            pass
        return actor_name

    def add_genre(self, genre: Genre):
        if genre not in self.__genre:
            self.__genre.append(genre)
            self.__genre_dict[genre] = genre

    def get_genre(self, genre_name) -> Genre:
        genre = None
        try:
            genre = self.__genre_dict[Genre(genre_name)]
        except KeyError:
            pass
        return genre

    def add_director(self, director: Director):
        if director not in self.__directors:
            self.__directors.append(director)
            self.__directors_dict[director] = director

    def get_director(self, director_name: str) -> Director:
        director = None
        try:
            director = self.__directors_dict[Director(director_name)]
        except KeyError:
            pass
        return director


def read_csv_file(file_path: str, repo: MemoryRepository):
    with open(os.path.join(file_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csvfile:
        # Rank,Title,Genre,Description,Director,Actors,Year,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore
        movie_file_reader = csv.DictReader(csvfile)

        index = 0
        for row in movie_file_reader:

            title = row['Title']
            release_year = int(row['Year'])
            repo.add_movie(Movie(title, release_year))

            actors = [Actor(actor.strip()) for actor in row['Actors'].split(",")]
            for actor in actors:
                repo.add_actor(actor)

            director = Director(row['Director'])
            repo.add_director(director)

            genres = [Genre(genre.strip()) for genre in row['Genre'].split(",")]
            for genre in genres:
                repo.add_genre(genre)

            # print(f"Movie {index} with title: {title}, release year {release_year}")
            index += 1


def populate(data_path: str, repo: MemoryRepository):
    read_csv_file(data_path, repo)


