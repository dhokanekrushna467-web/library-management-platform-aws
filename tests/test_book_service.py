import pytest

from app.services.library_service import LibraryService


@pytest.fixture
def service():
    library = LibraryService()
    library.reset()
    yield library
    library.reset()


def test_get_seeded_books(service):
    books = service.get_all_books()

    assert len(books) == 2
    assert service.get_book("B001")["title"] == (
        "Cloud Native DevOps Architecture"
    )


def test_search_books_by_title(service):
    results = service.search_books("DevOps")

    assert len(results) == 1
    assert results[0]["book_id"] == "B001"


def test_search_books_by_author(service):
    results = service.search_books("Linus Torvalds")

    assert len(results) == 1
    assert results[0]["book_id"] == "B001"


def test_search_books_by_isbn(service):
    results = service.search_books("978-0321601919")

    assert len(results) == 1
    assert results[0]["book_id"] == "B002"


def test_search_is_case_insensitive(service):
    assert len(service.search_books("devops")) == 1


def test_add_book(service):
    book = service.add_book(
        "B003",
        "Python Testing",
        "Test Author",
        "978-0000000001",
        4,
    )

    assert book["total_copies"] == 4
    assert book["available_copies"] == 4


def test_duplicate_book_rejected(service):
    with pytest.raises(ValueError, match="already exists"):
        service.add_book(
            "B001",
            "Another Title",
            "Another Author",
            "978-0000000002",
        )


def test_invalid_copy_count_rejected(service):
    with pytest.raises(ValueError, match="positive integer"):
        service.add_book(
            "B003",
            "Invalid Book",
            "Test Author",
            "978-0000000003",
            0,
        )


def test_missing_book(service):
    assert service.get_book("B999") is None


def test_delete_book(service):
    service.add_book(
        "B003",
        "Temporary Book",
        "Test Author",
        "978-0000000004",
    )

    assert service.delete_book("B003") is True
    assert service.get_book("B003") is None


def test_delete_missing_book_rejected(service):
    with pytest.raises(ValueError, match="not found"):
        service.delete_book("B999")
