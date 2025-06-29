# app.py
from flask import Flask, request, jsonify, render_template
import pandas as pd
import sqlite3
import google.generativeai as genai
import os
import tempfile
from dotenv import load_dotenv

# Load env variables
load_dotenv()
api_key = os.getenv("GENAI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Create Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# SQL query function
def sql_query(query: str):
    return pd.read_sql_query(query, connection).to_dict(orient='records')

# System prompt
system_prompt = """
You are an expert product recommender and SQL analyst.

You can use the following table:

- mytable:
  - product (string)
  - category (string)
  - sub_category (string)
  - brand (string)
  - sale_price (float)
  - market_price (float)
  - type (string)
  - rating (float)
  - description (string)

When user asks for product recommendations, follow this process:

1. If the user mentions a category or sub_category that matches exact values in the database, use those.
2. If the user mentions features that may appear in description (like "for dry hair", "moisturizing", "anti-aging"), include a `WHERE description LIKE '%keyword%'` clause in the SQL.
3. Always prioritize products with high ratings and good value (low sale_price vs market_price).
4. Return the results as friendly natural language recommendations.

Example:

User: Recommend products for dry hair

You should query:

SELECT product, brand, sale_price, rating, description
FROM mytable
WHERE category LIKE '%Hair Care%'
  OR sub_category LIKE '%Hair%'
  OR description LIKE '%dry hair%'
ORDER BY rating DESC
LIMIT 5;

Then format the response as:

Here are some great products for dry hair:
1. Product A (4.6, ₹250) — 'Nourishing shampoo for dry hair...'
2. Product B (4.5, ₹300) — 'Moisturizing conditioner for dry scalp...'
""".strip()

# Routes
@app.route('/')
def home():
    return render_template('index.html')  # frontend form

@app.route('/upload', methods=['POST'])
def upload():
    global connection, sql_gemini, chat

    # Get uploaded file
    uploaded_file = request.files['file']
    if not uploaded_file:
        return jsonify({'error': 'No file uploaded'}), 400

    # Save temp file
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
    uploaded_file.save(csv_path)

    # Load CSV into SQLite
    df = pd.read_csv(csv_path)
    df = df[['product', 'category', 'sub_category', 'brand', 'sale_price',
             'market_price', 'type', 'rating', 'description']]

    connection = sqlite3.connect('mydatabase.db', check_same_thread=False)
    df.to_sql('mytable', connection, if_exists='replace', index=False)

    # Set up Gemini model
    sql_gemini = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_prompt,
        tools=[sql_query]
    )
    chat = sql_gemini.start_chat(enable_automatic_function_calling=True)

    return jsonify({'message': 'CSV uploaded and model is ready!'})

@app.route('/query', methods=['POST'])
def query():
    global chat

    data = request.json
    user_question = data.get('question', '')

    if not user_question:
        return jsonify({'error': 'No question provided'}), 400

    response = chat.send_message(user_question)

    return jsonify({
        'question': user_question,
        'response': response.text
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)


