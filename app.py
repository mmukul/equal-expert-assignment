
import requests
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/<username>")
def get_gists(username):
    try:
        url = f"https://api.github.com/users/{username}/gists"

        response = requests.get(url, timeout=15)

        if response.status_code == 404:
            return jsonify({"error": "GitHub user not found"}), 404

        response.raise_for_status()
        return jsonify(response.json()), 200

    except requests.RequestException:
        return jsonify({"error": "Unable to connect to GitHub API"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
