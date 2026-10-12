from flask import Blueprint, jsonify, request

from app.services.library_service import LibraryService

api = Blueprint("api", __name__, url_prefix="/api")
library = LibraryService()


def error_response(message, status_code):
    return jsonify({"error": message}), status_code


@api.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "UP",
        "service": "Enterprise Smart Library Management Platform",
        "version": "1.0.0",
    }), 200


@api.route("/users", methods=["POST"])
def register_user():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("A JSON request body is required", 400)

    required = ("user_id", "name", "email")
    if any(not data.get(field) for field in required):
        return error_response(
            "user_id, name and email are required", 400
        )

    try:
        user = library.add_user(
            user_id=data["user_id"],
            name=data["name"],
            email=data["email"],
            role=data.get("role", "Student"),
        )
        return jsonify(user), 201
    except ValueError as exc:
        return error_response(str(exc), 400)


@api.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    user = library.get_user(user_id)

    if user is None:
        return error_response("User not found", 404)

    return jsonify(user), 200


@api.route("/books", methods=["GET"])
def get_books():
    query = request.args.get("q")
    return jsonify(library.get_all_books(query)), 200


@api.route("/books", methods=["POST"])
def add_book():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("A JSON request body is required", 400)

    required = ("book_id", "title", "author", "isbn")
    if any(not data.get(field) for field in required):
        return error_response(
            "book_id, title, author and isbn are required", 400
        )

    try:
        book = library.add_book(
            book_id=data["book_id"],
            title=data["title"],
            author=data["author"],
            isbn=data["isbn"],
            total_copies=data.get("total_copies", 1),
        )
        return jsonify(book), 201
    except ValueError as exc:
        return error_response(str(exc), 400)


@api.route("/borrow", methods=["POST"])
def borrow_book():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("A JSON request body is required", 400)

    if not data.get("user_id") or not data.get("book_id"):
        return error_response("user_id and book_id are required", 400)

    try:
        loan = library.borrow_book(data["user_id"], data["book_id"])
        return jsonify(loan), 200
    except ValueError as exc:
        return error_response(str(exc), 400)


@api.route("/return", methods=["POST"])
def return_book():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return error_response("A JSON request body is required", 400)

    if not data.get("user_id") or not data.get("book_id"):
        return error_response("user_id and book_id are required", 400)

    try:
        loan = library.return_book(data["user_id"], data["book_id"])
        return jsonify(loan), 200
    except ValueError as exc:
        return error_response(str(exc), 400)
