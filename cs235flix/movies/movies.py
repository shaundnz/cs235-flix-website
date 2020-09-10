from flask import Blueprint, render_template

movies_blueprint =Blueprint("movies_bp", __name__)

@movies_blueprint.route('/', methods=['GET'])
def movies():
    return render_template(
        'movies/movies.html'
    )