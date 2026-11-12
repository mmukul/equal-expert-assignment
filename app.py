import os
import requests
from flask import Flask, jsonify

app = Flask(__name__)

GITHUB_API = "https://api.github.com"


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/<username>")
def get_gists(username):
    if not username or len(username) > 39:
        return jsonify({"error": "Invalid GitHub username"}), 400

    url = f"{GITHUB_API}/users/{username}/gists"

    try:
        response = requests.get(
            url,
            headers={"Accept": "application/vnd.github+json"},
            timeout=15,
        )

        if response.status_code == 404:
            return jsonify({"error": "GitHub user not found"}), 404

        response.raise_for_status()
        return jsonify(response.json()), 200

    except requests.RequestException:
        app.logger.exception("GitHub API request failed")
        return jsonify({"error": "GitHub API is unavailable"}), 502
    except ValueError:
        return jsonify({"error": "Invalid response from GitHub"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
