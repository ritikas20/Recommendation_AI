from flask import Blueprint
from .home import home_bp
from .upload import upload_bp
from .query import query_bp

def register_routes(app):
    app.register_blueprint(home_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(query_bp)
