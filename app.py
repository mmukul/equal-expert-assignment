import os
import re

import requests
from flask import Flask, jsonify

app = Flask(__name__)

GITHUB_API_BASE = "https://api.github.com"
GITHUB_API_VERSION = "2026-03-10"
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$")


@app.get("/<username>")
def get_user_gists(username):
    """Return the public Gists for a GitHub username."""
    if not USERNAME_PATTERN.fullmatch(username):
        return jsonify({"error": "Invalid GitHub username"}), 400

    url = f"{GITHUB_API_BASE}/users/{username}/gists"
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": GITHUB_API_VERSION,
    }

    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"

    try:
        response = requests.get(
            url,
            headers=headers,
            params={"per_page": 100},
            timeout=10,
        )
    except requests.RequestException:
        app.logger.exception("Unable to reach GitHub API")
        return jsonify({"error": "GitHub API is unavailable"}), 502

    if response.status_code == 404:
        return jsonify({"error": "GitHub user not found"}), 404
    if response.status_code != 200:
        app.logger.error("GitHub API returned status %s", response.status_code)
        return jsonify({"error": "GitHub API request failed"}), 502

    try:
        gists = response.json()
    except ValueError:
        return jsonify({"error": "Invalid response from GitHub API"}), 502

    if not isinstance(gists, list):
        return jsonify({"error": "Unexpected response from GitHub API"}), 502

    return jsonify(gists), 200


@app.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "8080")))
