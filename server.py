from flask import Flask, request, jsonify
from flask_cors import CORS  # Importing CORS
import requests
from bs4 import BeautifulSoup
import pdfplumber

app = Flask(__name__)
CORS(app)  # This enables CORS for all routes

# Function to check if URL is a PDF
def is_pdf(url):
    return url.lower().endswith('.pdf')

# Function to extract text from PDF
def extract_pdf_text(url):
    response = requests.get(url)
    with pdfplumber.open(response.content) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.get_json()
        urls = data.get('urls')

        scraped_data = []
        for url in urls:
            if is_pdf(url):
                content = extract_pdf_text(url)
            else:
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                content = soup.get_text()

            scraped_data.append({"url": url, "content": content})

        return jsonify({"scraped_data": scraped_data})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")  # Ensures the server is accessible externally
