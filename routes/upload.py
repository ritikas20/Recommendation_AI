import os
import pandas as pd
from flask import Blueprint, request, jsonify, current_app
from database import init_db
from model import init_model

upload_bp = Blueprint('upload', __name__)

#Upload route to handle CSV file uploads
@upload_bp.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files.get('file')
    if not uploaded_file:
        return jsonify({'error': 'No file uploaded'}), 400

    csv_path = os.path.join(current_app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(csv_path)

    df = pd.read_csv(csv_path)
    df = df[['product', 'category', 'sub_category', 'brand', 'sale_price',
             'market_price', 'type', 'rating', 'description']]

    init_db(df)
    init_model()

    return jsonify({'message': 'CSV uploaded and model is ready!'})
