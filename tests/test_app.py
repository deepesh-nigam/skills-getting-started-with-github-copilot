"""Comprehensive FastAPI tests using Arrange-Act-Assert (AAA) pattern."""

from fastapi.testclient import TestClient


def test_root_redirect(client: TestClient):
    # Arrange
    # (TestClient fixture is preconfigured)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities(client: TestClient):
    # Arrange

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success(client: TestClient):
    # Arrange
    email = "aaaa@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]
    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_activity_not_found(client: TestClient):
    # Arrange
    email = "bbb@mergington.edu"
    activity = "Not Real Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_signup_already_registered(client: TestClient):
    # Arrange
    email = "michael@mergington.edu"  # pre-existing participant in Chess Club
    activity = "Chess Club"

    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_unregister_success(client: TestClient):
    # Arrange
    email = "michael@mergington.edu"  # pre-existing participant
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]
    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_signed_up(client: TestClient):
    # Arrange
    email = "nope@mergington.edu"
    activity = "Chess Club"

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_activity_not_found(client: TestClient):
    # Arrange
    email = "ccc@mergington.edu"
    activity = "Missing Club"

    # Act
    response = client.delete(f"/activities/{activity}/unregister", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
