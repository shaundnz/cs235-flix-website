from flask import Blueprint, render_template, request, url_for
import cs235flix.adapters.repository as repo
import cs235flix.movies.services as services

movies_blueprint =Blueprint("movies_bp", __name__)

movies_per_page = 3

# This is the home page, will show all movies in rank order
@movies_blueprint.route('/movies', methods=['GET'])
def movies():

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


    return render_template(
        'movies/movies.html',
        movies_page_title = "Browsing movies",
        movies = movies_dict,
        first_movie_url=first_movie_url,
        last_movie_url = last_movie_url,
        next_movie_url = next_movie_url,
        prev_movie_url = prev_movie_url,
        )

@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    genre_name = request.args.get('genre')
    current_page = request.args.get('page')

    if current_page is None:
        current_page = 1

    current_page = int(current_page)

    first_page = 1
    last_page = services.get_number_pages_for_genre(genre_name, movies_per_page, repo.repo_instance)

    movies_dict, prev_page, next_page = services.get_next_n_movies_for_genre(genre_name, current_page, movies_per_page, repo.repo_instance)

    first_page_url = None
    last_page_url = None
    next_page_url = None
    prev_page_url = None


    if len(movies_dict) > 0:
        if prev_page is not None:
            prev_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name, page = prev_page)
            first_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name, page = first_page)
        if next_page is not None:
            next_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name, page = next_page)
            last_page_url = url_for('movies_bp.movies_by_genre', genre=genre_name, page = last_page)

    return render_template(
        'movies/movies.html',
        movies_page_title="Browsing movies with tag: " + genre_name,
        movies=movies_dict,
        first_movie_url=first_page_url,
        last_movie_url=last_page_url,
        next_movie_url=next_page_url,
        prev_movie_url=prev_page_url,
    )















