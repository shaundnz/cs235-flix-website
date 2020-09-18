from flask import Blueprint, request, render_template, url_for, redirect
from cs235flix.search import services
import cs235flix.adapters.repository as repo
from cs235flix.services import get_movie_poster_url

search_blueprint = Blueprint('search_bp', __name__)
results_per_page = 3
match_threshold = 0.2

@search_blueprint.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('q')
    page = request.args.get('page')

    if page is None:
        page = 1

    page = int(page)

    first_page = 1

    movies_dict, prev_page, next_page, last_page, number_results = services.get_next_n_search_results(search_query, match_threshold, page,
                                                                                 results_per_page, repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if len(movies_dict) > 0:
        if prev_page is not None:
            prev_movie_url = url_for('search_bp.search', q=search_query, page=prev_page)
            first_movie_url = url_for('search_bp.search', q=search_query, page=first_page)
        if next_page is not None:
            next_movie_url = url_for('search_bp.search', q=search_query, page=next_page)
            last_movie_url = url_for('search_bp.search', q=search_query, page=last_page)

        for movie in movies_dict:
            movie['add_review_url'] = url_for('movies_bp.review_movie', title = movie['title'], year=movie['release_year'])
            movie['poster_url'] = get_movie_poster_url(movie['title'], movie['release_year'])

    
    return render_template(
        'movies/movies.html',
        movies_page_title = "Search for " + search_query + " yielded " + str(number_results) + " results",
        movies = movies_dict,
        first_movie_url=first_movie_url,
        last_movie_url = last_movie_url,
        next_movie_url = next_movie_url,
        prev_movie_url = prev_movie_url,
        )


