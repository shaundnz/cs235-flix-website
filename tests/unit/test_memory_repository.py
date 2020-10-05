import pytest

from cs235flix.domainmodel.actor import Actor
from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.review import Review
from cs235flix.domainmodel.user import User
from cs235flix.domainmodel.director import Director
from cs235flix.domainmodel.genre import Genre


def test_add_movie(in_mem_repo):
    m = Movie("Fake Movie", 2020)
    in_mem_repo.add_movie(m)
    assert in_mem_repo.get_movie("Fake Movie", 2020) is m


def test_get_movie(in_mem_repo):
    m = in_mem_repo.get_movie("Guardians of the Galaxy", 2014)
    assert m == Movie("Guardians of the Galaxy", 2014)


def test_get_non_existent_movie(in_mem_repo):
    m = in_mem_repo.get_movie("I dont exist", 2015)
    assert m is None


def test_get_movie_by_index(in_mem_repo):
    m1 = in_mem_repo.get_movie_by_index(0)
    m2 = in_mem_repo.get_movie_by_index(4)
    assert m1 == Movie("Guardians of the Galaxy", 2014)
    assert m2 == Movie("Suicide Squad", 2016)


def test_get_movie_by_invalid_index(in_mem_repo):
    assert in_mem_repo.get_movie_by_index(150) is None


def test_get_number_movies(in_mem_repo):
    assert in_mem_repo.get_number_movies() == 100


def test_get_all_movies(in_mem_repo):
    assert len(in_mem_repo.get_all_movies()) == 100
    assert in_mem_repo.get_all_movies()[0] == Movie("Guardians of the Galaxy", 2014)
    assert in_mem_repo.get_all_movies()[99] == Movie("The Departed", 2006)


def test_add_actor(in_mem_repo):
    a = Actor("John Doe")
    in_mem_repo.add_actor(a)
    assert in_mem_repo.get_actor("John Doe") is a


def test_get_actor(in_mem_repo):
    a = in_mem_repo.get_actor("Chris Pratt")
    assert a == Actor("Chris Pratt")


def test_get_non_existent_actor(in_mem_repo):
    assert in_mem_repo.get_actor("Fake Actor") is None


def test_add_director(in_mem_repo):
    d = Director("John Doe")
    in_mem_repo.add_director(d)
    assert in_mem_repo.get_director("John Doe") is d


def test_get_director(in_mem_repo):
    d = in_mem_repo.get_director("Christopher Nolan")
    assert d == Director("Christopher Nolan")


def test_get_non_existent_director(in_mem_repo):
    assert in_mem_repo.get_director("Fake Director") is None


def test_add_genre(in_mem_repo):
    g = Genre("Documentary")
    in_mem_repo.add_genre(g)
    assert in_mem_repo.get_genre("Documentary") is g


def test_get_genre(in_mem_repo):
    g = in_mem_repo.get_genre("Action")
    assert g == Genre("Action")


def test_get_non_existent_genre(in_mem_repo):
    assert in_mem_repo.get_genre("Fake Genre") is None


def test_get_num_genre(in_mem_repo):
    assert in_mem_repo.get_number_genres() == 18


def test_get_genre_by_index(in_mem_repo):
    assert in_mem_repo.get_genre_by_index(0) == Genre("Action")
    assert in_mem_repo.get_genre_by_index(5) == Genre("Thriller")
    assert in_mem_repo.get_genre_by_index(17) == Genre("War")


def test_get_number_movies_for_genre(in_mem_repo):
    action_movies_num = in_mem_repo.get_number_movies_for_genre(Genre("Action"))
    assert action_movies_num == 39


def test_get_movies_for_genre(in_mem_repo):
    thriller_movies = in_mem_repo.get_movies_for_genre(Genre("Thriller"))
    for movie in thriller_movies:
        assert Genre("Thriller") in movie.genres


def test_add_user(in_mem_repo):
    u = User("newuser1", "password")
    in_mem_repo.add_user(u)
    assert in_mem_repo.get_user("newuser1") is u


def test_get_user(in_mem_repo):
    u = User("newuser2", "pw12345")
    in_mem_repo.add_user(u)
    assert in_mem_repo.get_user("newuser2") == User("newuser2", "pw12345")


def test_get_non_existent_user(in_mem_repo):
    assert in_mem_repo.get_user("fakeuser") is None


def test_add_review(in_mem_repo):
    u = User("newuser1", "password")
    in_mem_repo.add_user(u)
    r = Review(Movie("Guardians of the Galaxy", 2014), "This is the review text", 9, "newuser1")
    in_mem_repo.add_review(r, "newuser1")
    assert r in in_mem_repo.get_reviews()
    assert r in in_mem_repo.get_user("newuser1").reviews
    assert r in in_mem_repo.get_movie("Guardians of the Galaxy", 2014).reviews


def test_get_reviews_for_movie(in_mem_repo):
    u1 = User("newuser1", "password")
    in_mem_repo.add_user(u1)
    r1 = Review(Movie("Guardians of the Galaxy", 2014), "This is the review text", 9, "newuser1")
    u2= User("newuser2", "password")
    in_mem_repo.add_user(u2)
    r2 = Review(Movie("Guardians of the Galaxy", 2014), "This is the other review", 2, "newuser2")

    in_mem_repo.add_review(r1, "newuser1")
    in_mem_repo.add_review(r2, "newuser2")

    assert len(in_mem_repo.get_reviews_for_movie(Movie("Guardians of the Galaxy", 2014))) == 2
    assert r1 in in_mem_repo.get_reviews_for_movie(Movie("Guardians of the Galaxy", 2014))
    assert r2 in in_mem_repo.get_reviews_for_movie(Movie("Guardians of the Galaxy", 2014))