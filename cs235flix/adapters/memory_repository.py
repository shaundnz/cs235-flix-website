import os
from typing import List
import csv

from cs235flix.adapters.repository import AbstractRepository
from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.actor import Actor
from cs235flix.domainmodel.director import Director
from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.review import Review
from cs235flix.domainmodel.user import User


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__movies = list()
        self.__movies_dict = dict()

        self.__genres = list()
        self.__genres_dict = dict()

        self.__actors = list()
        self.__actors_dict = dict()

        self.__directors = list()
        self.__directors_dict = dict()

        self.__users = list()

        self.__reviews = list()

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

    def get_all_movies(self):
        return self.__movies


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
        return actor

    def add_genre(self, genre: Genre):
        if genre not in self.__genres:
            self.__genres.append(genre)
            self.__genres_dict[genre] = genre

    def get_genre(self, genre_name) -> Genre:
        genre = None
        try:
            genre = self.__genres_dict[Genre(genre_name)]
        except KeyError:
            pass
        return genre

    def get_all_genres(self):
        return self.__genres

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

    def get_number_movies(self):
        return len(self.__movies)

    def get_movie_by_index(self, index: int):
        movie = None
        if index < len(self.__movies):
            movie = self.__movies[index]
        return movie

    def get_number_genres(self):
        return len(self.__genres)

    def get_genre_by_index(self, index: int):
        genre = None
        if index < len(self.__genres):
            genre = self.__genres[index]
        return genre

    def get_number_movies_for_genre(self, genre: Genre):
        total = 0
        for movie in self.__movies:
            if genre in movie.genres:
                total += 1
        return total

    def get_movies_for_genre(self, genre: Genre):
        movies = list()
        for movie in self.__movies:
            if genre in movie.genres:
                movies.append(movie)
        return movies

    def add_user(self, user: User):
        self.__users.append(user)

    def get_user(self, username) -> User:
        for user in self.__users:
            if username == user.username:
                return user
        return None

    def add_review(self, review: Review, username):
        self.__reviews.append(review)
        for user in self.__users:
            if user.username == username:
                user.add_review(review)
        for movie in self.__movies:
            if movie == review.movie:
                movie.add_review(review)

    def get_reviews_for_movie(self, movie: Movie):
        reviews = list()
        for review in self.__reviews:
            if review.movie == movie:
                reviews.append(review)
        return reviews

    def get_reviews(self):
        return self.__reviews

def read_csv_file(data_path: str, movie_data_filename, repo: MemoryRepository):
    with open(os.path.join(data_path, movie_data_filename), mode='r', encoding='utf-8-sig') as csvfile:
        # Rank,Title,Genre,Description,Director,Actors,Year,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore
        movie_file_reader = csv.DictReader(csvfile)

        index = 0
        for row in movie_file_reader:

            repo.add_movie(create_movie_instance(row))

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

    with open(os.path.join(data_path, "users.csv"), mode='r', encoding='utf-8-sig') as csvfile:
        # Unhashed passwords, shaunp:pw123456, fellowuser:password123

        user_file_reader = csv.DictReader(csvfile)
        for row in user_file_reader:
            repo.add_user(User(row['username'], row['password']))

def create_movie_instance(row):
    movie = Movie(row["Title"], int(row["Year"]))
    movie.director = Director(row["Director"])
    movie.runtime_minutes = int(row["Runtime (Minutes)"])
    movie.actors = [Actor(actor.strip()) for actor in row['Actors'].split(",")]
    movie.genres = [Genre(genre.strip()) for genre in row['Genre'].split(",")]
    movie.description = row["Description"]
    return movie


def populate(data_path: str, movie_data_filename, repo: MemoryRepository):
    read_csv_file(data_path, movie_data_filename, repo)


