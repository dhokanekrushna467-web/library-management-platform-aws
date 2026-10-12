from app.models.book import Book
from app.models.user import User


def test_book_default_available_copies():
    book = Book("B101", "Test Book", "Test Author", 5)

    assert book.available_copies == 5
    assert book.to_dict()["book_id"] == "B101"


def test_book_custom_available_copies():
    book = Book(
        "B102",
        "Another Book",
        "Another Author",
        5,
        2,
    )

    assert book.available_copies == 2
    assert book.to_dict()["total_copies"] == 5


def test_user_default_role_and_active_status():
    user = User("U103", "Test Student", "student@example.com")

    assert user.role == "Student"
    assert user.active is True
    assert user.to_dict()["user_id"] == "U103"


def test_user_custom_role():
    user = User(
        "U104",
        "Test Faculty",
        "faculty@example.com",
        "Faculty",
    )

    assert user.role == "Faculty"
    assert user.to_dict()["email"] == "faculty@example.com"
