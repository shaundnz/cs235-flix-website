from cs235flix.adapters.repository import AbstractRepository
import math


def get_number_pages(n, repo: AbstractRepository):
    return math.ceil(repo.get_number_genres() / n)


def get_next_n_genres(current_page, n, repo: AbstractRepository):
    genres = list()
    page = int(current_page)
    prev_page = next_page = None

    if page*n <= repo.get_number_genres():
        for i in range(n):
            genres.append(repo.get_genre_by_index((page - 1) * n + i).genre_name)
    else:
        for i in range((repo.get_number_genres() % ((page - 1)*n))):
            genres.append(repo.get_genre_by_index((page - 1) * n + i).genre_name)

    if page > 1:
        prev_page = page - 1
    if page < get_number_pages(n, repo):
        next_page = page + 1

    return genres, prev_page, next_page
