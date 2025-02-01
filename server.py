from flask import Flask, render_template, request
import requests
from googlesearch import search
import os

app = Flask(__name__)

# Function to search for PDFs
def search_pdfs(topic, author=None, keywords=None):
    query = f"{topic} filetype:pdf"
    if author:
        query += f" {author}"
    if keywords:
        query += f" {' '.join(keywords)}"

    print(f"Searching for PDFs with query: {query}")
    results = search(query, num=5)  # Fetch more results

    pdf_links = [result for result in results if result.endswith(".pdf")]
    return pdf_links

# Function to download PDFs
def download_pdf(url, download_folder="static/pdf_downloads"):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            os.makedirs(download_folder, exist_ok=True)
            filename = os.path.join(download_folder, url.split("/")[-1])
            with open(filename, 'wb') as file:
                file.write(response.content)
            return filename  # Return the local file path
        else:
            return None
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return None

# Flask route to handle the form and search results
@app.route('/', methods=['GET', 'POST'])
def index():
    pdf_links = []
    downloaded_files = []
    
    if request.method == 'POST':
        topic = request.form['topic']
        author = request.form.get('author', '')
        keywords = request.form.get('keywords', '')

        keywords_list = [kw.strip() for kw in keywords.split(",")] if keywords else None
        
        pdf_links = search_pdfs(topic, author, keywords_list)

        # Download PDFs automatically
        for link in pdf_links:
            downloaded_file = download_pdf(link)
            if downloaded_file:
                downloaded_files.append(downloaded_file)

    return render_template('index.html', pdf_links=pdf_links, downloaded_files=downloaded_files)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
