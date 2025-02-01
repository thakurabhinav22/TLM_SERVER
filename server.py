from flask import Flask, request, jsonify
from flask_cors import CORS  # To handle CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Route to handle search request
@app.route('/search', methods=['POST'])
def search():
    try:
        # Get data from the POST request
        data = request.get_json()
        topic = data.get('topic')
        author = data.get('author', '')
        keywords = data.get('keywords', '')

        # You can add logic here to process the data and fetch PDF links
        # For now, let's return a dummy response
        pdf_links = [
            f"https://example.com/{topic}_pdf1.pdf",
            f"https://example.com/{topic}_pdf2.pdf"
        ]

        response = {
            "topic": topic,
            "pdf_links": pdf_links
        }

        return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)  # Make sure to adjust the port if necessary
