import json, urllib.parse, urllib.request
import math

from flask import url_for

from cs235flix.domainmodel.movie import Movie


def get_movie_poster_url(movie_title, release_year):
    API_KEY = '6654c5ee'
    url = 'http://www.omdbapi.com/?apikey=' + API_KEY + '&t=' + urllib.parse.quote(movie_title) + '&y=' + str(
        release_year)
    data = json.load(urllib.request.urlopen(url))

    # Hard coding an unknown title
    if movie_title == "Taare Zameen Par":
        movie_title = 'Like Stars on Earth'

    try:
        poster_url = data['Poster']
        poster_url = poster_url.replace('300', '600')
    except KeyError:
        poster_url = url_for('static', filename='images/image-not-found.jpg')

    return poster_url


def get_page_items(current_page, results_per_page, item_list):
    page_items = list()
    page = int(current_page)
    prev_page = next_page = None
    if page * results_per_page <= len(item_list):
        for i in range(results_per_page):
            page_items.append(item_list[(current_page - 1) * results_per_page + i])
    else:
        for i in range(len(item_list) % max(((page - 1) * results_per_page), results_per_page)):
            page_items.append(item_list[(current_page - 1) * results_per_page + i])
    if page > 1:
        prev_page = page - 1
    if page < get_number_pages(results_per_page, len(item_list)):
        next_page = page + 1
    return page_items, prev_page, next_page


def get_number_pages(results_per_page, item_list_len):
    return math.ceil(item_list_len / results_per_page)


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
