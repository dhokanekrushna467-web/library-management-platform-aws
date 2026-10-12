from database.db import db


class LibraryService:
    def __init__(self):
        self.db = db

    def reset(self):
        self.db.reset()

    def add_user(self, user_id, name, email, role="Student"):
        with self.db.lock:
            if user_id in self.db.users:
                raise ValueError("User already exists")

            if role not in ("Student", "Faculty"):
                raise ValueError("Role must be Student or Faculty")

            user = {
                "user_id": user_id,
                "name": name,
                "email": email,
                "role": role,
                "active": True,
                "active_loans": 0,
            }

            self.db.users[user_id] = user
            return user.copy()

    def get_user(self, user_id):
        with self.db.lock:
            user = self.db.users.get(user_id)
            return user.copy() if user else None

    def add_book(
        self,
        book_id,
        title,
        author,
        isbn,
        total_copies=1,
    ):
        with self.db.lock:
            if book_id in self.db.books:
                raise ValueError("Book already exists")

            if (
                not isinstance(total_copies, int)
                or isinstance(total_copies, bool)
                or total_copies < 1
            ):
                raise ValueError(
                    "Total copies must be a positive integer"
                )

            book = {
                "book_id": book_id,
                "title": title,
                "author": author,
                "isbn": isbn,
                "total_copies": total_copies,
                "available_copies": total_copies,
            }

            self.db.books[book_id] = book
            return book.copy()

    def get_book(self, book_id):
        with self.db.lock:
            book = self.db.books.get(book_id)
            return book.copy() if book else None

    def get_all_books(self, query=None):
        with self.db.lock:
            books = list(self.db.books.values())

            if query:
                query = query.casefold()
                books = [
                    book for book in books
                    if (
                        query in book["title"].casefold()
                        or query in book["author"].casefold()
                        or query in book["isbn"].casefold()
                    )
                ]

            return [book.copy() for book in books]

    def search_books(self, query):
        return self.get_all_books(query)

    def delete_book(self, book_id):
        with self.db.lock:
            book = self.db.books.get(book_id)

            if book is None:
                raise ValueError("Book not found")

            if book["available_copies"] != book["total_copies"]:
                raise ValueError(
                    "Cannot delete a book with active loans"
                )

            del self.db.books[book_id]
            return True

    def borrow_book(self, user_id, book_id):
        with self.db.lock:
            user = self.db.users.get(user_id)
            book = self.db.books.get(book_id)

            if user is None or not user["active"]:
                raise ValueError("Active user not found")

            if book is None:
                raise ValueError("Book not found")

            loan_limit = 3 if user["role"] == "Student" else 5

            if user["active_loans"] >= loan_limit:
                raise ValueError(
                    "User has reached the borrowing limit"
                )

            if book["available_copies"] < 1:
                raise ValueError("No copies available")

            self.db.loan_counter += 1

            loan = {
                "loan_id": f"L-{self.db.loan_counter:04d}",
                "user_id": user_id,
                "book_id": book_id,
                "status": "ACTIVE",
                "borrowed_at": None,
                "returned_at": None,
            }

            book["available_copies"] -= 1
            user["active_loans"] += 1
            self.db.loans.append(loan)

            return loan.copy()

    def return_book(self, user_id, book_id):
        with self.db.lock:
            for loan in self.db.loans:
                if (
                    loan["user_id"] == user_id
                    and loan["book_id"] == book_id
                    and loan["status"] == "ACTIVE"
                ):
                    loan["status"] = "RETURNED"
                    loan["returned_at"] = None

                    self.db.books[book_id]["available_copies"] += 1
                    self.db.users[user_id]["active_loans"] -= 1

                    return loan.copy()

            raise ValueError(
                "No active loan found for this user and book"
            )
