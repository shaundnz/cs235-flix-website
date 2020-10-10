import pytest

from cs235flix.domainmodel.genre import Genre
from cs235flix.domainmodel.movie import Movie
from cs235flix.domainmodel.user import User
from cs235flix.services import get_movie_poster_url, get_number_pages, get_page_items
from cs235flix.movies.services import get_page_items_movies, get_page_items_movies_for_genre, get_number_pages_movies, \
    get_number_pages_movies_for_genre, add_review
from cs235flix.authentication.services import add_user, authenticate_user, get_user, check_password_hash, \
    UnknownUserException, NameNotUniqueException, AuthenticationException

from cs235flix.search.services import build_movie_string, levenshtein_ratio, partial_ratio, token_set_ratio, \
    get_page_items_movies_search


def test_get_valid_poster_movie_url():
    assert get_movie_poster_url("Guardians of the Galaxy", 2014) == \
           "https://m.media-amazon.com/images/M/MV5BMTAwMjU5OTgxNjZeQTJeQWpwZ15BbWU4MDUxNDYxODEx._V1_SX600.jpg", \
        "This may fail if the API is down, visit OMDB to check"


def test_get_page_items():
    big_list = [i for i in range(1, 1001)]
    small_list = [i for i in range(1, 5)]

    assert get_page_items(1, 6, big_list) == ([1, 2, 3, 4, 5, 6], None, 2)
    assert get_page_items(167, 6, big_list) == ([997, 998, 999, 1000], 166, None)
    assert get_page_items(20, 5, big_list) == ([96, 97, 98, 99, 100], 19, 21)

    assert get_page_items(1, 10, small_list) == ([1, 2, 3, 4], None, None)


def test_get_number_pages():
    assert get_number_pages(6, 1000) == 167
    assert get_number_pages(5, 10) == 2
    assert get_number_pages(10, 5) == 1


def test_get_number_pages_movies(in_mem_repo):
    assert get_number_pages_movies(1, in_mem_repo) == 100
    assert get_number_pages_movies(2, in_mem_repo) == 50
    assert get_number_pages_movies(3, in_mem_repo) == 34
    assert get_number_pages_movies(110, in_mem_repo) == 1


def test_get_number_pages_movies_for_genre(in_mem_repo):
    assert get_number_pages_movies_for_genre("Comedy", 3, in_mem_repo) == 8
    assert get_number_pages_movies_for_genre("Comedy", 25, in_mem_repo) == 1
    assert get_number_pages_movies_for_genre("Horror", 5, in_mem_repo) == 2


def test_get_first_page_items_movies(in_mem_repo):
    m_tuple = get_page_items_movies(1, 2, in_mem_repo)
    assert m_tuple[0][0]['title'] == "Guardians of the Galaxy"
    assert m_tuple[0][0]['release_year'] == 2014
    assert m_tuple[0][1]['title'] == "Prometheus"
    assert m_tuple[0][1]['release_year'] == 2012
    assert m_tuple[1] is None
    assert m_tuple[2] == 2


def test_get_middle_page_items_movies(in_mem_repo):
    m_tuple = get_page_items_movies(3, 2, in_mem_repo)
    assert m_tuple[0][0]['title'] == "Suicide Squad"
    assert m_tuple[0][0]['release_year'] == 2016
    assert m_tuple[0][1]['title'] == "The Great Wall"
    assert m_tuple[0][1]['release_year'] == 2016
    assert m_tuple[1] == 2
    assert m_tuple[2] == 4


def test_get_last_page_items_movies(in_mem_repo):
    m_tuple = get_page_items_movies(50, 2, in_mem_repo)
    assert m_tuple[0][0]['title'] == "Personal Shopper"
    assert m_tuple[0][0]['release_year'] == 2016
    assert m_tuple[0][1]['title'] == "The Departed"
    assert m_tuple[0][1]['release_year'] == 2006
    assert len(m_tuple[0]) == 2
    assert m_tuple[1] == 49
    assert m_tuple[2] is None


def test_get_first_page_items_movies_for_genre(in_mem_repo):
    m_tuple = get_page_items_movies_for_genre("Comedy", 1, 3, in_mem_repo)
    assert m_tuple[0][0]['title'] == "Sing"
    assert m_tuple[0][1]['title'] == "La La Land"
    assert m_tuple[0][2]['title'] == "Mindhorn"
    assert m_tuple[1] is None
    assert m_tuple[2] == 2


def test_get_middle_page_items_movies_for_genre(in_mem_repo):
    m_tuple = get_page_items_movies_for_genre("Comedy", 4, 3, in_mem_repo)
    assert m_tuple[0][0]['title'] == "Why Him?"
    assert m_tuple[0][1]['title'] == "Deadpool"
    assert m_tuple[0][2]['title'] == "5- 25- 77"
    assert m_tuple[1] is 3
    assert m_tuple[2] == 5


def test_get_last_page_items_movies_for_genre(in_mem_repo):
    m_tuple = get_page_items_movies_for_genre("Comedy", 8, 3, in_mem_repo)
    assert m_tuple[0][0]['title'] == "The Nice Guys"
    assert len(m_tuple[0]) == 1
    assert m_tuple[1] is 7
    assert m_tuple[2] == None


def test_add_review(in_mem_repo):
    add_review("Split", 2016, "cool movie", 8, "testuser", in_mem_repo)
    assert len(in_mem_repo.get_reviews_for_movie(Movie("Split", 2016))) == 2
    assert in_mem_repo.get_reviews_for_movie(Movie("Split", 2016))[1].review_text == "cool movie"
    assert in_mem_repo.get_reviews_for_movie(Movie("Split", 2016))[1].rating == 8


def test_get_user(in_mem_repo):
    user = get_user("shaunp", in_mem_repo)
    assert user['username'] == "shaunp"
    assert check_password_hash(user['password'], "pw123456")


def test_get_user_does_not_exist(in_mem_repo):
    with pytest.raises(UnknownUserException):
        get_user("fakeuser", in_mem_repo)


def test_add_user(in_mem_repo):
    add_user("testuser", "password", in_mem_repo)
    assert in_mem_repo.get_user("testuser").username == "testuser"


def test_add_user_name_not_unique(in_mem_repo):
    with pytest.raises(NameNotUniqueException):
        add_user("shaunp", "password", in_mem_repo)


def test_authenticate_user(in_mem_repo):
    assert authenticate_user("shaunp", "pw123456", in_mem_repo) is True


def test_authenticate_user_password_does_not_match(in_mem_repo):
    with pytest.raises(AuthenticationException):
        authenticate_user("shaunp", "pw654321", in_mem_repo)


def test_build_movie_string(in_mem_repo):
    m = in_mem_repo.get_movie("Guardians of the Galaxy", 2014)
    assert build_movie_string(m) == "Guardians of the Galaxy 2014 Chris Pratt Vin Diesel Bradley Cooper " \
                                    "Zoe Saldana James Gunn"


def test_lev_ratio():
    assert levenshtein_ratio("hello there", "general kenobi, you are a bold one") < 0.5
    assert levenshtein_ratio("Chris Pratt", "Chris Prat") > 0.9
    assert levenshtein_ratio("I am groot", "I am groot") == 1


def test_partial_ratio():
    assert partial_ratio("bush", "bush") == 1
    assert partial_ratio("GeorgeWBush", "Bush") > 0.6
    assert partial_ratio("lakers", "lake") > 0.6
    assert partial_ratio("hello", "there") == 0


def test_token_set_ratio():
    assert token_set_ratio("George W Bush", "Im a bush") > 0.6
    assert token_set_ratio("Guardians of the Galaxy 2014 Chris Pratt Vin Diesel Bradley Cooper", "Galaxy") == 1
    assert token_set_ratio("Guardians of the Galaxy 2014 Chris Pratt Vin Diesel Bradley Cooper", "Hemsworth") < 0.3


def test_get_page_items_movies_search(in_mem_repo):
    result = get_page_items_movies_search("Pratt", 0.2, 1, 5, in_mem_repo)
    expected_results = ("Guardians of the Galaxy", "The Magnificent Seven", "Jurassic World", "Passengers")
    assert len(result) == 5
    assert result[0][0]['title'] in expected_results
    assert result[0][1]['title'] in expected_results
    assert result[0][2]['title'] in expected_results
    assert result[0][3]['title'] in expected_results
    assert result[1] is None

