import pytest

from app.services.library_service import LibraryService


@pytest.fixture
def service():
    library = LibraryService()
    library.reset()
    yield library
    library.reset()


def test_get_seeded_student(service):
    user = service.get_user("U101")

    assert user is not None
    assert user["name"] == "Alice Johnson"
    assert user["role"] == "Student"
    assert user["active"] is True


def test_get_seeded_faculty(service):
    user = service.get_user("U102")

    assert user is not None
    assert user["name"] == "Dr. Robert Smith"
    assert user["role"] == "Faculty"


def test_get_missing_user(service):
    assert service.get_user("U999") is None


def test_add_student(service):
    user = service.add_user(
        "U103",
        "Test Student",
        "student@university.edu",
        "Student",
    )

    assert user["user_id"] == "U103"
    assert user["active"] is True
    assert service.get_user("U103")["name"] == "Test Student"


def test_add_faculty(service):
    user = service.add_user(
        "U104",
        "Test Faculty",
        "faculty@university.edu",
        "Faculty",
    )

    assert user["role"] == "Faculty"


def test_duplicate_user_rejected(service):
    with pytest.raises(ValueError, match="already exists"):
        service.add_user(
            "U101",
            "Duplicate User",
            "duplicate@university.edu",
        )


def test_invalid_role_rejected(service):
    with pytest.raises(ValueError, match="Role"):
        service.add_user(
            "U105",
            "Invalid User",
            "invalid@university.edu",
            "Visitor",
        )
