from flask import Flask, render_template, request
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

    # Using a loop to get a fixed number of results instead of 'num'
    pdf_links = []
    for result in search(query):  # Default fetches results iteratively
        if result.endswith(".pdf"):
            pdf_links.append(result)
        if len(pdf_links) >= 5:  # Limit to 5 results manually
            break

    return pdf_links

@app.route('/', methods=['GET', 'POST'])
def index():
    pdf_links = []
    
    if request.method == 'POST':
        topic = request.form['topic']
        author = request.form.get('author', '')
        keywords = request.form.get('keywords', '')

        keywords_list = [kw.strip() for kw in keywords.split(",")] if keywords else None
        
        pdf_links = search_pdfs(topic, author, keywords_list)

    return render_template('index.html', pdf_links=pdf_links)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
