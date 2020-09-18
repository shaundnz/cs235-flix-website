import json, urllib.parse, urllib.request

from flask import url_for


def get_movie_poster_url(movie_title, release_year):
    API_KEY = '6654c5ee'
    url = 'http://www.omdbapi.com/?apikey=' + API_KEY + '&t=' + urllib.parse.quote(movie_title) + '&y=' + str(release_year)
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




