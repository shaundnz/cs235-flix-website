from flask import Blueprint, render_template, request, url_for, session, redirect
from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, SubmitField, HiddenField

import cs235flix.adapters.repository as repo
import cs235flix.movies.services as services
from cs235flix.authentication.authentication import login_required

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

        for movie in movies_dict:
            movie['add_review_url'] = url_for('movies_bp.review_movie', title = movie['title'], year=movie['release_year'])

        return render_template(
            'movies/movies.html',
            movies_page_title = "Browsing movies",
            movies = movies_dict,
            first_movie_url=first_movie_url,
            last_movie_url = last_movie_url,
            next_movie_url = next_movie_url,
            prev_movie_url = prev_movie_url,
            )

    return redirect(url_for('home_bp.home'))

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

        for movie in movies_dict:
            movie['add_review_url'] = url_for('movies_bp.review_movie', title = movie['title'], year=movie['release_year'])

        return render_template(
            'movies/movies.html',
            movies_page_title="Browsing movies with tag: " + genre_name,
            movies=movies_dict,
            first_movie_url=first_page_url,
            last_movie_url=last_page_url,
            next_movie_url=next_page_url,
            prev_movie_url=prev_page_url,
        )

    return redirect(url_for('home_bp.home'))

@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_movie():
    username = session['username']

    form = CommentForm()

    if form.validate_on_submit():
        movie_title = form.movie_title.data
        movie_release_year = int(form.movie_release_year.data)

        services.add_review(movie_title, movie_release_year, form.review_text.data, form.review_rating.data, username, repo.repo_instance)
        return redirect(url_for('home_bp.home'))


    if request.method == 'GET':
        movie_title = request.args.get('title')
        movie_release_year = int(request.args.get('year'))

        form.movie_title.data = movie_title
        form.movie_release_year.data = movie_release_year
    else:
        movie_title = form.movie_title.data
        movie_release_year = int(form.movie_release_year.data)

    title = "Review for: " + movie_title + " (" + str(movie_release_year) + ")"

    return render_template(
        'movies/movie_reviews.html',
        title = title,
        form = form,
        handler_url = url_for('movies_bp.review_movie')
    )



class CommentForm(FlaskForm):
    movie_title = HiddenField('Movie title')
    movie_release_year = HiddenField('Release year')
    review_text = TextAreaField('Review')
    review_rating = IntegerField('Rating out of 10')
    submit = SubmitField('Post review')













