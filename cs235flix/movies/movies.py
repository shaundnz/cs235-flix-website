from flask import Blueprint, render_template, request, url_for
import cs235flix.adapters.repository as repo
import cs235flix.movies.services as services

movies_blueprint =Blueprint("movies_bp", __name__)

# This is the home page, will show all movies in rank order
@movies_blueprint.route('/movies', methods=['GET'])
def movies():

    movies_per_page = 5

    current_page = request.args.get('page')

    if current_page is None:
        current_page = 1

    first_page = 1
    last_page = services.get_number_pages(movies_per_page, repo.repo_instance)

    movies_dict, prev_page, next_page = services.get_next_n_movies(current_page, movies_per_page, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies_dict) > 0:
        if prev_page is not None:
            prev_movie_url = url_for('movies_bp.movies', page=prev_page)
            first_movie_url = url_for('movies_bp.movies', page=first_page)
        if next_page is not None:
            next_movie_url = url_for('movies_bp.movies', page=next_page)
            last_movie_url = url_for('movies_bp.movies', page=last_page)

    print(movies_dict)


    return render_template(
        'movies/movies.html',
        movies = movies_dict,
        first_movie_url=first_movie_url,
        last_movie_url = last_movie_url,
        next_movie_url = next_movie_url,
        prev_movie_url = prev_movie_url,
        )