from typing import List
import math
from cs235flix.adapters.memory_repository import AbstractRepository
from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.review import Review
from cs235flix.domainmodel.user import User
from cs235flix.services import movie_to_dict, get_page_items, get_number_pages


class MovieNotFoundException:
    pass


def movies_to_dict(movies: List[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def get_page_items_movies(current_page_str, results_per_page, repo: AbstractRepository):
    movies_obj_list, prev_page, next_page = get_page_items(int(current_page_str), results_per_page,
                                                           repo.get_all_movies())
    return movies_to_dict(movies_obj_list), prev_page, next_page


def get_page_items_movies_for_genre(genre, current_page_str, results_per_page, repo: AbstractRepository):
    movies_obj_list, prev_page, next_page = get_page_items(int(current_page_str), results_per_page,
                                                           repo.get_movies_for_genre(Genre(genre)))
    return movies_to_dict(movies_obj_list), prev_page, next_page


def get_number_pages_movies(results_per_page, repo: AbstractRepository):
    return get_number_pages(results_per_page, repo.get_number_movies())


def get_number_pages_movies_for_genre(genre, results_per_page, repo: AbstractRepository):
    return get_number_pages(results_per_page, repo.get_number_movies_for_genre(Genre(genre)))


def add_review(movie_title, movie_release_year, review_text, review_rating, username, repo: AbstractRepository):
    review = Review(Movie(movie_title, movie_release_year), review_text, review_rating, username)
    repo.add_review(review, username)
