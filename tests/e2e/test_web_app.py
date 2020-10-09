import pytest

from flask import session


def test_register(client):
    resp_code = client.get('/authentication/register').status_code
    assert resp_code == 200

    resp = client.post(
        '/authentication/register',
        data={'username': 'testuser', 'password': 'Password1234'}
    )

    assert resp.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('username', 'password', 'message'), (
        ('', '', b'Your username is required'),
        ('cj', '', b'Your username is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test', b'Your password must be at least 8 characters, and contain an upper case letter, '
                         b'a lower case letter and a digit'),
        ('shaunp', 'Test#6^0', b'Your username is already taken - please supply another'),
))
def test_register_with_invalid_input(client, username, password, message):
    # Check that attempting to register with invalid combinations of username and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'username': username, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['username'] == 'shaunp'


def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'CS235FLIX' in response.data


def test_review(client, auth):
    auth.login()

    resp = client.get('/review?title=Guardians+of+the+Galaxy&year=2014')

    resp = client.post('/review?title=Guardians+of+the+Galaxy&year=2014',
                       data={'review_text': 'Nice', 'review_rating': 5})

    assert resp.headers['Location'] == 'http://localhost/review?title=Guardians+of+the+Galaxy&year=2014'


def test_review_not_logged_in(client):
    resp = client.get('/review?title=Guardians+of+the+Galaxy&year=2014')

    resp = client.post('/review?title=Guardians+of+the+Galaxy&year=2014',
                       data={'review_text': 'Nice', 'review_rating': 5})

    assert resp.headers['Location'] == 'http://localhost/authentication/login'


def test_review_invalid_input(client, auth):
    auth.login()
    resp = client.post('/review?title=Guardians+of+the+Galaxy&year=2014',
                       data={'review_text': 'Nice', 'review_rating': 50})

    assert b'Please enter a number between 1 and 10' in resp.data

    resp = client.post('/review?title=Guardians+of+the+Galaxy&year=2014',
                       data={'review_text': 'Nice', 'review_rating': -50})

    assert b'Please enter a number between 1 and 10' in resp.data


def test_movie_page(client):
    resp = client.get('/movies')
    m = [b"Guardians", b"Split", b"Suicide Squad"]
    for movie in m:
        assert movie in resp.data


def test_movie_genre_page(client):
    resp = client.get('/movies_by_genre?genre=Horror')
    assert b'Horror' in resp.data

def test_genre_page(client):
    resp = client.get('/genres')
    assert b'Action' in resp.data
    assert b'Comedy' in resp.data
