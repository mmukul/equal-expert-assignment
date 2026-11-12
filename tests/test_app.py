import unittest
from unittest.mock import Mock, patch

import requests

from app import app


class GitHubGistsApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("app.requests.get")
    def test_returns_public_gists_for_user(self, mock_get):
        expected = [
            {
                "id": "gist-123",
                "description": "Example public gist",
                "public": True,
                "html_url": "https://gist.github.com/octocat/gist-123",
            }
        ]
        response_from_github = Mock(status_code=200)
        response_from_github.json.return_value = expected
        mock_get.return_value = response_from_github

        response = self.client.get("/octocat")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), expected)
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        self.assertEqual(
            args[0], "https://api.github.com/users/octocat/gists"
        )
        self.assertEqual(kwargs["params"], {"per_page": 100})
        self.assertEqual(kwargs["timeout"], 10)

    @patch("app.requests.get")
    def test_returns_404_when_github_user_does_not_exist(self, mock_get):
        mock_get.return_value = Mock(status_code=404)

        response = self.client.get("/this-user-should-not-exist-12345")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            response.get_json(), {"error": "GitHub user not found"}
        )

    @patch("app.requests.get")
    def test_returns_502_when_github_is_unavailable(self, mock_get):
        mock_get.side_effect = requests.Timeout()

        response = self.client.get("/octocat")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.get_json(), {"error": "GitHub API is unavailable"}
        )

    @patch("app.requests.get")
    def test_returns_502_for_non_success_github_response(self, mock_get):
        mock_get.return_value = Mock(status_code=403)

        response = self.client.get("/octocat")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.get_json(), {"error": "GitHub API request failed"}
        )

    @patch("app.requests.get")
    def test_returns_502_for_invalid_github_json(self, mock_get):
        github_response = Mock(status_code=200)
        github_response.json.side_effect = ValueError("invalid JSON")
        mock_get.return_value = github_response

        response = self.client.get("/octocat")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(
            response.get_json(), {"error": "Invalid response from GitHub API"}
        )

    @patch("app.requests.get")
    def test_rejects_invalid_username_without_calling_github(self, mock_get):
        response = self.client.get("/bad username")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Invalid GitHub username"})
        mock_get.assert_not_called()

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})


if __name__ == "__main__":
    unittest.main()
