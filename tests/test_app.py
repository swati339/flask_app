import pytest
from app.main import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_hello_world(client):
    response = client.get('/')
    assert response.data == b'Hello, World!'
    assert response.status_code == 200

def test_add_task(client):
    response = client.get('/add-task')
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'job_id' in json_data
