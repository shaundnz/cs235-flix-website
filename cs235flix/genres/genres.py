from flask import Blueprint, render_template, request, url_for
import cs235flix.adapters.repository as repo
import cs235flix.genres.services as services
from cs235flix.services import get_number_pages, get_page_items

genres_blueprint = Blueprint('genres_bp', __name__)


@genres_blueprint.route('/genres', methods=['GET'])
def genres():
    genres_per_page = 8

    current_page = request.args.get('page')

    if current_page is None:
        current_page = 1

    current_page = int(current_page)

    first_page = 1
    last_page = get_number_pages(genres_per_page, repo.repo_instance.get_number_genres())

    genres_list, prev_page, next_page = get_page_items(current_page, genres_per_page, repo.repo_instance.get_all_genres())

    first_page_url = None
    last_page_url = None
    next_page_url = None
    prev_page_url = None

    if len(genres_list) > 0:
        if prev_page is not None:
            first_page_url = url_for('genres_bp.genres', page=first_page)
            prev_page_url = url_for('genres_bp.genres', page=prev_page)
        if next_page is not None:
            last_page_url = url_for('genres_bp.genres', page=last_page)
            next_page_url = url_for('genres_bp.genres', page=next_page)

    return render_template(
        'genres/genres.html',
        genres=genres_list,
        first_page_url=first_page_url,
        last_page_url=last_page_url,
        next_page_url=next_page_url,
        prev_page_url=prev_page_url
    )
