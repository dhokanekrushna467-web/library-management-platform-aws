import pytest

from app.services.library_service import LibraryService


@pytest.fixture
def service():
    library = LibraryService()
    library.reset()
    yield library
    library.reset()


def test_borrow_book_successfully(service):
    loan = service.borrow_book("U101", "B001")

    assert loan["status"] == "ACTIVE"
    assert loan["user_id"] == "U101"
    assert loan["book_id"] == "B001"


def test_borrow_decreases_available_copies(service):
    service.borrow_book("U101", "B001")

    assert service.get_book("B001")["available_copies"] == 4


def test_borrow_increases_active_loan_count(service):
    service.borrow_book("U101", "B001")

    assert service.get_user("U101")["active_loans"] == 1


def test_return_book_successfully(service):
    service.borrow_book("U101", "B001")
    loan = service.return_book("U101", "B001")

    assert loan["status"] == "RETURNED"


def test_return_restores_available_copies(service):
    service.borrow_book("U101", "B001")
    service.return_book("U101", "B001")

    assert service.get_book("B001")["available_copies"] == 5


def test_return_decreases_active_loan_count(service):
    service.borrow_book("U101", "B001")
    service.return_book("U101", "B001")

    assert service.get_user("U101")["active_loans"] == 0


def test_student_borrowing_limit(service):
    service.borrow_book("U101", "B001")
    service.borrow_book("U101", "B002")
    service.add_book("B003", "Book Three", "Author", "ISBN003")
    service.borrow_book("U101", "B003")

    service.add_book("B004", "Book Four", "Author", "ISBN004")

    with pytest.raises(ValueError, match="borrowing limit"):
        service.borrow_book("U101", "B004")


def test_faculty_borrowing_limit(service):
    service.add_book("B003", "Book Three", "Author", "ISBN003")
    service.add_book("B004", "Book Four", "Author", "ISBN004")
    service.add_book("B005", "Book Five", "Author", "ISBN005")

    service.borrow_book("U102", "B001")
    service.borrow_book("U102", "B002")
    service.borrow_book("U102", "B003")
    service.borrow_book("U102", "B004")
    service.borrow_book("U102", "B005")

    service.add_book("B006", "Book Six", "Author", "ISBN006")

    with pytest.raises(ValueError, match="borrowing limit"):
        service.borrow_book("U102", "B006")


def test_borrow_missing_book_rejected(service):
    with pytest.raises(ValueError, match="Book not found"):
        service.borrow_book("U101", "B999")


def test_borrow_missing_user_rejected(service):
    with pytest.raises(ValueError, match="user not found"):
        service.borrow_book("U999", "B001")


def test_return_without_active_loan_rejected(service):
    with pytest.raises(ValueError, match="No active loan"):
        service.return_book("U101", "B001")


def test_book_cannot_be_deleted_while_borrowed(service):
    service.borrow_book("U101", "B001")

    with pytest.raises(ValueError, match="active loans"):
        service.delete_book("B001")


def test_returned_loan_cannot_be_returned_twice(service):
    service.borrow_book("U101", "B001")
    service.return_book("U101", "B001")

    with pytest.raises(ValueError, match="No active loan"):
        service.return_book("U101", "B001")
