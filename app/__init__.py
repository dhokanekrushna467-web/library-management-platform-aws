from flask import Flask, jsonify, render_template


def create_app(test_config=None):
    app = Flask(__name__)

    @app.route("/")
    def dashboard():
        return render_template("index.html")

    if test_config:
        app.config.update(test_config)

    from app.routes.api import api
    app.register_blueprint(api)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"error": "Internal server error"}), 500

    return app
