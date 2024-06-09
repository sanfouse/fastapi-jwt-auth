from tests.client import client


def test_users_all():
    response = client.get("/users")
    assert response.status_code == 200
