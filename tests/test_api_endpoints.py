import pytest

from app import create_app
from app.services.library_service import LibraryService


@pytest.fixture
def client():
    library = LibraryService()
    library.reset()

    app = create_app({"TESTING": True})
    with app.test_client() as test_client:
        yield test_client

    library.reset()


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_get_all_books(client):
    response = client.get("/api/books")

    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_search_books(client):
    response = client.get("/api/books?q=DevOps")

    assert response.status_code == 200
    assert len(response.get_json()) == 1
    assert response.get_json()[0]["book_id"] == "B001"


def test_get_existing_user(client):
    response = client.get("/api/users/U101")

    assert response.status_code == 200
    assert response.get_json()["name"] == "Alice Johnson"


def test_get_missing_user(client):
    response = client.get("/api/users/U999")

    assert response.status_code == 404


def test_register_user(client):
    response = client.post(
        "/api/users",
        json={
            "user_id": "U103",
            "name": "Test Student",
            "email": "test@university.edu",
            "role": "Student",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["user_id"] == "U103"


def test_register_user_missing_fields(client):
    response = client.post(
        "/api/users",
        json={"user_id": "U103"},
    )

    assert response.status_code == 400


def test_add_book(client):
    response = client.post(
        "/api/books",
        json={
            "book_id": "B003",
            "title": "Python Testing",
            "author": "Test Author",
            "isbn": "978-0000000001",
            "total_copies": 2,
        },
    )

    assert response.status_code == 201
    assert response.get_json()["available_copies"] == 2


def test_borrow_book(client):
    response = client.post(
        "/api/borrow",
        json={"user_id": "U101", "book_id": "B001"},
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "ACTIVE"


def test_return_book(client):
    client.post(
        "/api/borrow",
        json={"user_id": "U101", "book_id": "B001"},
    )

    response = client.post(
        "/api/return",
        json={"user_id": "U101", "book_id": "B001"},
    )

    assert response.status_code == 200
    assert response.get_json()["status"] == "RETURNED"


def test_borrow_missing_book(client):
    response = client.post(
        "/api/borrow",
        json={"user_id": "U101", "book_id": "B999"},
    )

    assert response.status_code == 400


def test_borrow_missing_fields(client):
    response = client.post(
        "/api/borrow",
        json={"user_id": "U101"},
    )

    assert response.status_code == 400


def test_register_duplicate_user(client):
    response = client.post(
        "/api/users",
        json={
            "user_id": "U101",
            "name": "Duplicate User",
            "email": "duplicate@university.edu",
        },
    )

    assert response.status_code == 400
