import unittest
from unittest.mock import Mock, patch

from app import app


class GistsApiTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "ok"})

    @patch("app.requests.get")
    def test_get_user_gists(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = [{"id": "123", "description": "Example gist"}]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response = self.client.get("/octocat")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()[0]["id"], "123")
        mock_get.assert_called_once()

    @patch("app.requests.get")
    def test_github_user_not_found(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = self.client.get("/this-user-should-not-exist")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.get_json()["error"], "GitHub user not found")


if __name__ == "__main__":
    unittest.main()
