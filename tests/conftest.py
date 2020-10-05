import os
import pytest

from cs235flix import create_app
from cs235flix.adapters import memory_repository
from cs235flix.adapters.memory_repository import MemoryRepository

TEST_DATA_PATH = os.path.join('tests', 'data', 'Data100Movies.csv')

@pytest.fixture
def in_mem_repo():
    repo = MemoryRepository()
    memory_repository.populate(TEST_DATA_PATH, repo)
    return repo

@pytest.fixture
def client():
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False
    })

    return my_app.test_client()

# TODO Get auth manager working
class AuthenticationManage:
    def __init__(self, client):
        self._client = client


