from flask import Flask, jsonify, request
from flask_cors import CORS
from .database import get_db_connection

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return jsonify({"message": "Assignment 11 Multi-Tier Backend API"})


@app.route("/api/users", methods=["GET"])
def get_users():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT id, name, email FROM users")
    users = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(users)


@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "name and email are required"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()

    query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    cursor.execute(query, (data["name"], data["email"]))

    connection.commit()

    user_id = cursor.lastrowid

    cursor.close()
    connection.close()

    return jsonify({
        "id": user_id,
        "name": data["name"],
        "email": data["email"],
    }), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
