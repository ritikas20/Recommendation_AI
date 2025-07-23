from flask import Flask
from routes import register_routes
from config import configure_app

app = Flask(__name__)
configure_app(app)
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
