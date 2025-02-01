from flask import Flask, request, jsonify

app = Flask(__name__)

# Route to accept the POST request and greet the user
@app.route('/greet', methods=['POST'])
def greet_user():
    try:
        # Get JSON data from the request
        data = request.get_json()

        # Extract the 'name' field from the incoming JSON
        name = data.get("name")

        if not name:
            return jsonify({"error": "Name is required"}), 400
        
        # Respond with a greeting message
        greeting_message = f"Hello, {name}! Welcome to the server!"
        return jsonify({"message": greeting_message}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
