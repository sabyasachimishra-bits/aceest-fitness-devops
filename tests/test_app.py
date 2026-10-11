import pytest

from app import create_app


@pytest.fixture()
def app(tmp_path):
    database_file = tmp_path / "test_aceest.db"

    application = create_app(
        {
            "TESTING": True,
            "DATABASE": str(database_file),
        }
    )

    yield application


@pytest.fixture()
def client(app):
    return app.test_client()


def test_home_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"ACEest Functional Fitness System" in response.data
    assert b"Fat Loss (FL)" in response.data
    assert b"Muscle Gain (MG)" in response.data
    assert b"Beginner (BG)" in response.data


def test_health_endpoint(client):
    response = client.get("/health")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["status"] == "healthy"
    assert payload["application"] == "ACEest Fitness and Gym"


def test_programs_endpoint(client):
    response = client.get("/api/programs")
    payload = response.get_json()

    assert response.status_code == 200
    assert "Fat Loss (FL)" in payload
    assert "Muscle Gain (MG)" in payload
    assert payload["Beginner (BG)"]["calorie_factor"] == 26


def test_fat_loss_calculation(client):
    response = client.post(
        "/api/calories",
        json={
            "program": "Fat Loss (FL)",
            "weight": 80,
        },
    )

    payload = response.get_json()

    assert response.status_code == 200
    assert payload["estimated_calories"] == 1760


def test_muscle_gain_calculation(client):
    response = client.post(
        "/api/calories",
        json={
            "program": "Muscle Gain (MG)",
            "weight": 80,
        },
    )

    payload = response.get_json()

    assert response.status_code == 200
    assert payload["estimated_calories"] == 2800


def test_invalid_program_rejected(client):
    response = client.post(
        "/api/calories",
        json={
            "program": "Unknown",
            "weight": 75,
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Invalid fitness program"


def test_non_numeric_weight_rejected(client):
    response = client.post(
        "/api/calories",
        json={
            "program": "Beginner (BG)",
            "weight": "invalid",
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Weight must be numeric"


def test_create_and_retrieve_client(client):
    create_response = client.post(
        "/clients",
        data={
            "name": "DevOps Student",
            "age": "30",
            "weight": "70",
            "program": "Beginner (BG)",
        },
    )

    assert create_response.status_code == 201
    assert create_response.get_json()["estimated_calories"] == 1820

    list_response = client.get("/api/clients")
    clients = list_response.get_json()

    assert list_response.status_code == 200
    assert len(clients) == 1
    assert clients[0]["name"] == "DevOps Student"
    assert clients[0]["program"] == "Beginner (BG)"
