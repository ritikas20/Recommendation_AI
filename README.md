## AI Recommendation System

![Screenshot (4)](https://github.com/user-attachments/assets/1a4f3e99-44e4-4c33-8c42-66617cc6b037)
# 🛍️ Product Recommender with Gemini + Semantic SQL Matching

An AI-powered product recommendation system that converts natural language queries into smart, SQL-driven answers. Combines Google Gemini's language capabilities with semantic similarity search and MySQL for accurate, personalized recommendations.

---

## 🚀 Features

- ✅ Upload a CSV file of product data
- 🧠 Ask natural language questions like:
  > “Suggest me a product for frizzy hair under the lowest price”
- 🤖 Uses **LLM + Embeddings** to recommend the most relevant product
- 🗃️ Queries product data stored in **MySQL**, not just in memory
- 📊 Clean web interface with Flask

---

## 🧠 Technical Approach

- 🔍 **Natural Language to SQL Query Generation**  
  User questions are dynamically interpreted and translated into **SQL queries**, targeting structured data in a MySQL database.

- 🤝 **Few-shot Learning with SemanticSimilarityExampleSelector**  
  Implemented **few-shot prompting** using `SemanticSimilarityExampleSelector`, enabling the LLM to handle complex queries involving **joins** and **multi-attribute conditions**.

- 🧬 **Semantic Matching with HuggingFace + ChromaDB**  
  Used **HuggingFace sentence-transformer embeddings** to compute semantic similarity between user queries and existing examples.  
  Integrated **ChromaDB** to perform efficient vector search, increasing recommendation accuracy by **25%** over traditional keyword search.

---




