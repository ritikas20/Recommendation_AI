from flask import Blueprint, request, jsonify
from model import chat

query_bp = Blueprint('query', __name__)

@query_bp.route('/query', methods=['POST'])
def query():
    data = request.json
    user_question = data.get('question', '')

    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    response = chat.send_message(user_question)
    return jsonify({
        'question': user_question,
        'response': response.text
    })
