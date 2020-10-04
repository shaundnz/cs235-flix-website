import pytest

from cs235flix.domainmodel.actor import Actor
from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.review import Review
from cs235flix.domainmodel.user import User
from cs235flix.domainmodel.director import Director
from cs235flix.domainmodel.genre import Genre


# Test Actors
@pytest.fixture
def actors_list():
    actors_list = [Actor("John Doe"),
                   Actor("Jane Doe"),
                   Actor("John Doe"),
                   Actor(""),
                   Actor(12345)]
    return actors_list


def test_actor_repr(actors_list):
    assert repr(actors_list[0]) == "John Doe"
    assert repr(actors_list[1]) == "Jane Doe"
    assert repr(actors_list[2]) == "John Doe"
    assert repr(actors_list[3]) == "None"
    assert repr(actors_list[4]) == "None"


def test_actor_equality(actors_list):
    assert actors_list[0] == actors_list[0]
    assert actors_list[0] != actors_list[1]
    assert actors_list[0] == actors_list[2]
    assert actors_list[0] != actors_list[3]
    assert actors_list[3] == actors_list[4]


def test_actor_less_than(actors_list):
    assert (actors_list[0] < actors_list[1]) == ("John Doe" < "Jane Doe")
    assert (actors_list[0] < actors_list[2]) is False
    assert (actors_list[0] < actors_list[3]) == ("John Doe" < "")
    assert (actors_list[3] < actors_list[4]) is False


def test_actor_colleague(actors_list):
    assert actors_list[0].check_if_this_actor_worked_with(actors_list[2]) is False
    assert actors_list[0].check_if_this_actor_worked_with(actors_list[3]) is False
    actors_list[0].add_actor_colleague(actors_list[1])
    actors_list[0].add_actor_colleague(actors_list[3])
    assert actors_list[0].check_if_this_actor_worked_with(actors_list[1]) is True
    assert actors_list[0].check_if_this_actor_worked_with(actors_list[3]) is True
    assert actors_list[2].check_if_this_actor_worked_with(actors_list[1]) is False


# Test Directors
@pytest.fixture
def director_list():
    director_list = [Director("Jane Doe"),
                     Director("John Doe"),
                     Director("John Doe"),
                     Director(""),
                     Director(123)
                     ]
    return director_list


def test_director_init(director_list):
    assert repr(director_list[1]) == "John Doe"
    assert repr(director_list[3]) == "None"
    assert repr(director_list[4]) == "None"


def test_director_director_equality(director_list):
    assert director_list[0] != "Jane Doe"
    assert director_list[0] != 12345
    assert director_list[0] != director_list[1]
    assert director_list[1] == director_list[2]
    assert director_list[0] != director_list[4]
    assert director_list[0] == director_list[0]
    assert director_list[4] == director_list[4]


def test_director_less_than(director_list):
    assert (director_list[0] < director_list[1]) == ("Jane Doe" < "John Doe")
    assert (director_list[1] < director_list[3]) is False
    assert (director_list[0] < director_list[4]) == ("Jane Doe" < "")


def test_director_hash(director_list):
    assert hash(director_list[1]) == hash(director_list[2])
    assert hash(director_list[1]) != hash(director_list[0])
    assert hash(director_list[1]) != hash(director_list[4])


# Test Genre
@pytest.fixture
def genre_list():
    genre_list = [Genre("Horror"),
                  Genre("Comedy"),
                  Genre(""),
                  Genre(12345),
                  Genre("Horror")
                  ]
    return genre_list


def test_genre_repr(genre_list):
    assert repr(genre_list[0]) == "Horror"
    assert repr(genre_list[1]) == "Comedy"
    assert repr(genre_list[2]) == "None"
    assert repr(genre_list[3]) == "None"


def test_genre_equality(genre_list):
    assert genre_list[0] == genre_list[0]
    assert genre_list[0] != genre_list[1]
    assert genre_list[0] != genre_list[2]
    assert genre_list[0] != genre_list[3]
    assert genre_list[2] == genre_list[2]
    assert genre_list[2] == genre_list[3]
    assert genre_list[0] == genre_list[4]


def test_genre_less_than(genre_list):
    assert (genre_list[0] < genre_list[1]) == ("Horror" < "Comedy")
    assert (genre_list[0] < genre_list[2]) == ("Horror" < "")
    assert (genre_list[0] < genre_list[0]) == ("Horror" < "Horror")
    assert (genre_list[2] < genre_list[3]) is False
    assert (genre_list[0] < genre_list[4]) is False


def test_genre_hash(genre_list):
    assert hash(genre_list[0]) == hash(genre_list[4])
    assert hash(genre_list[2]) == hash(genre_list[3])
    assert hash(genre_list[0]) != hash(genre_list[1])
    assert hash(genre_list[0]) == hash(genre_list[0])


# Test Review
@pytest.fixture
def test_review():
    return Review(Movie("Movie Title", 2015), "This is the review test text", 9, "testuser1")

def test_review_init(test_review):
    assert test_review.movie == Movie("Movie Title", 2015)
    assert test_review.review_text == "This is the review test text"
    assert test_review.rating == 9
    assert test_review.username == "testuser1"

    r = Review(Movie("Movie Title", 2015), "This is the review test text", 150, "testuser1")
    assert r.rating is None

def test_review_repr(test_review):
    assert repr(test_review) == "<Movie: <Movie Movie Title, 2015> Rating: 9 Review: This is the review test text>"


# Test User
@pytest.fixture
def user_list():
    user_list = [
        User("testuser1", "1234"),
        User("testuser2", "5678"),
        User("testuser3", "password")
    ]
    return user_list

@pytest.fixture
def test_user():
    return User("thelegend27", "password")

def test_user_init():
    u = User("newuser", "password")
    assert u.username == "newuser"
    assert u.password == "password"
    assert u.time_spent_watching_movies == 0
    assert u.reviews == []
    assert u.watched_movies == []


def test_user_repr(user_list):
    assert repr(user_list[0]) == "<User testuser1>"
    assert repr(user_list[1]) == "<User testuser2>"


def test_user_equality(user_list):
    assert user_list[0] == user_list[0]
    assert user_list[0] != user_list[1]
    assert user_list[0] != "testuser1"
    assert user_list[2] == User("testuser3", "password")


def test_user_less_than(user_list):
    assert user_list[1] < user_list[2]
    assert not user_list[1] < user_list[1]
    assert not user_list[2] < user_list[1]


def test_user_hash(user_list):
    assert hash(user_list[0]) == hash(user_list[0])
    assert hash(user_list[0]) != hash(user_list[1])
    assert hash(user_list[0]) == hash(User("testuser1", "password"))


def test_user_movie(test_user):
    m1 = Movie("Movie 1", 2020)
    m1.runtime_minutes = 50
    m2 = Movie("Movie 2", 2020)
    m2.runtime_minutes = 80

    test_user.watch_movie(m1)
    test_user.watch_movie(m2)

    assert m1 in test_user.watched_movies
    assert m2 in test_user.watched_movies
    assert test_user.time_spent_watching_movies == 130


def test_user_review(test_user):
    r1 = Review(Movie("Movie 1", 2020), "test review", 8, test_user.username)
    r2 = Review(Movie("Movie 2", 2020), "Another review", 3, test_user.username)

    test_user.add_review(r1)
    test_user.add_review(r2)

    assert r1 in test_user.reviews
    assert r2 in test_user.reviews

    assert len(test_user.reviews) == 2
    test_user.add_review(r1)
    assert len(test_user.reviews) == 2


# Test Movie
@pytest.fixture
def movie_list():
    movie_list = [
        Movie("Casino Royale", 2006),
        Movie("Star Wars: A New Hope", 1977),
        Movie("The Matrix", 1999)
    ]
    return movie_list


@pytest.fixture
def test_movie():
    return Movie("Test Movie", 2020)


def test_movie_init(movie_list):
    assert movie_list[0].title == "Casino Royale"
    assert movie_list[0].release_year == 2006
    assert Movie("", 2006).title == None
    assert Movie(123, 2006).title == None
    with pytest.raises(ValueError):
        Movie("Movie Title", 1899)


def test_movie_repr(movie_list):
    assert repr(movie_list[0]) == "<Movie Casino Royale, 2006>"
    assert repr(movie_list[1]) == "<Movie Star Wars: A New Hope, 1977>"
    assert repr(movie_list[2]) == "<Movie The Matrix, 1999>"


def test_movie_equality(movie_list):
    assert movie_list[0] != movie_list[1]
    assert movie_list[1] != movie_list[2]
    assert movie_list[0] == movie_list[0]
    assert movie_list[1] == Movie("Star Wars: A New Hope", 1977)


def test_movie_less_than(movie_list):
    assert (movie_list[0] < movie_list[1]) is True
    assert (movie_list[1] < movie_list[2]) is True
    assert (movie_list[1] < movie_list[1]) is False


def test_movie_hash(movie_list):
    assert hash(movie_list[0]) == hash(movie_list[0])
    assert hash(movie_list[0]) != hash(movie_list[1])
    assert hash(movie_list[0]) == hash((Movie("Casino Royale", 2006)))


def test_movie_actor(test_movie):
    m = Movie("Movie Title", 2020)
    assert test_movie.actors == []
    a1 = Actor("John Doe")
    a2 = Actor("Jane Doe")
    test_movie.add_actor(a1)
    test_movie.add_actor(a2)
    assert a1 in test_movie.actors
    assert a2 in test_movie.actors
    test_movie.remove_actor(a1)
    assert a1 not in test_movie.actors
    assert a2 in test_movie.actors
    test_movie.remove_actor(a1)
    assert a1 not in test_movie.actors
    assert a2 in test_movie.actors


def test_movie_genre(test_movie):
    m = Movie("Movie Title", 2005)
    assert test_movie.genres == []
    g1 = Genre("Horror")
    g2 = Genre("Comedy")
    test_movie.add_genre(g1)
    test_movie.add_genre(g2)
    assert g1 in test_movie.genres
    assert g2 in test_movie.genres
    test_movie.remove_genre(g1)
    assert g1 not in test_movie.genres
    assert g2 in test_movie.genres
    test_movie.remove_genre(g1)
    assert g1 not in test_movie.genres
    assert g2 in test_movie.genres


def test_movie_director(test_movie):
    assert test_movie.director is None
    test_movie.director = Director("John Doe")
    assert test_movie.director == Director("John Doe")


def test_movie_review(test_movie):
    r1 = Review(test_movie, "Test review 1", 9, "testuser1")
    r2 = Review(test_movie, "Another review", 6, "testuser2")
    test_movie.add_review(r1)
    test_movie.add_review(r2)
    assert r1 in test_movie.get_reviews()
    assert r2 in test_movie.get_reviews()
    assert test_movie.get_reviews() == [r1, r2]
