from typing import List
import math
from cs235flix.adapters.memory_repository import AbstractRepository
from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.review import Review
from cs235flix.domainmodel.user import User


class MovieNotFoundException:
    pass


def movie_to_dict(movie: Movie):
    movie_dict = {
        'title': movie.title,
        'release_year': movie.release_year,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'genres': movie.genres,
        'runtime_minutes': movie.runtime_minutes,
        'reviews': movie.get_reviews()
    }
    return movie_dict


def movies_to_dict(movies: List[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def get_first_movie(repo: AbstractRepository):
    movie = repo.get_first_movie()
    if movie is None:
        raise MovieNotFoundException
    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):
    movie = repo.get_last_movie()
    if movie is None:
        raise MovieNotFoundException
    return movie_to_dict(movie)


def get_next_n_movies(page_str, n, repo: AbstractRepository):
    movies = list()
    page = int(page_str)
    prev_page = next_page = None
    if page * n <= repo.get_number_movies():
        for i in range(n):
            movies.append(movie_to_dict(repo.get_movie_by_index((page - 1) * n + i)))
    else:
        for i in range(repo.get_number_movies() % ((page - 1) * n)):
            movies.append(movie_to_dict(repo.get_movie_by_index((page - 1) * n + i)))
    if page > 1:
        prev_page = page - 1
    if page < get_number_pages(n, repo):
        next_page = page + 1
    return movies, prev_page, next_page


def get_next_n_movies_for_genre(genre, page_str, n, repo: AbstractRepository):
    all_movies = repo.get_movies_for_genre(Genre(genre))
    movies = list()
    page = int(page_str)
    prev_page = next_page = None

    if page * n <= len(all_movies):
        for i in range(n):
            movies.append(movie_to_dict(all_movies[((page - 1) * n + i)]))
    else:
        for i in range(len(all_movies) % ((page - 1) * n)):
            movies.append(movie_to_dict(all_movies[((page - 1) * n + i)]))

    if page > 1:
        prev_page = page - 1

    if page < get_number_pages_for_genre(genre, n, repo):
        next_page = page + 1

    return movies, prev_page, next_page


def get_number_pages(n, repo: AbstractRepository):
    return math.ceil(repo.get_number_movies() / n)


def get_number_pages_for_genre(genre, n, repo: AbstractRepository):
    return math.ceil(repo.get_number_movies_for_genre(Genre(genre)) / n)


def add_review(movie_title, movie_release_year, review_text, review_rating, username, repo: AbstractRepository):
    review = Review(Movie(movie_title, movie_release_year), review_text, review_rating, username)
    repo.add_review(review, username)
