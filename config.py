import os
import tempfile
from dotenv import load_dotenv
# set the environment variable for the upload folder
def configure_app(app):
    load_dotenv()
    app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()
    app.config['GENAI_API_KEY'] = os.getenv("GENAI_API_KEY")