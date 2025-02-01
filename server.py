from flask import Flask, request, jsonify
import requests
from googlesearch import search

app = Flask(__name__)

# Function to search for PDFs
def search_pdfs(topic, author=None, keywords=None):
    query = f"{topic} filetype:pdf"
    if author:
        query += f" {author}"
    if keywords:
        query += f" {' '.join(keywords)}"

    print(f"Searching for PDFs with query: {query}")

    pdf_links = []
    for result in search(query):  # Fetch search results iteratively
        if result.endswith(".pdf"):
            pdf_links.append(result)
        if len(pdf_links) >= 5:  # Limit to 5 results manually
            break

    return pdf_links

# API Endpoint to handle search
@app.route('/search', methods=['POST'])
def search_api():
    data = request.get_json()  # Get JSON data from POST request

    # Validate required fields
    if not data or 'topic' not in data:
        return jsonify({"error": "Topic is required"}), 400

    topic = data['topic']
    author = data.get('author', '')  # Optional field
    keywords = data.get('keywords', '')

    keywords_list = [kw.strip() for kw in keywords.split(",")] if keywords else None
    
    # Get PDF search results
    pdf_links = search_pdfs(topic, author, keywords_list)

    return jsonify({"topic": topic, "pdf_links": pdf_links})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
