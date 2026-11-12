# GitHub Public Gists API — Killercoda

A small Flask API that returns the public Gists for a GitHub username. The API listens on port `8080` and sends outbound GitHub HTTPS requests through the external HTTP proxy `172.30.1.2:8080`.

## Configuration

The proxy is configured in `docker-compose.yml`:

```yaml
environment:
  HTTPS_PROXY: http://172.30.1.2:8080
```

No proxy authentication is configured. The proxy must already be running, reachable from the Killercoda lab/container network, and support HTTP `CONNECT` to `api.github.com:443`.

**Network note:** `172.30.1.2` is a private IP address, not globally routable. If this IP belongs to a different lab, host, or network namespace, the API container may not be able to reach it. Confirm the address from the same Killercoda scenario/network in which this API runs.

## Run in Killercoda

From the project directory:

```bash
docker compose up --build -d
```

If Docker Compose is unavailable but Docker is installed:

```bash
docker build -t github-gists-api .
docker run -d --name github-gists-api \\
  -p 8080:8080 \\
  -e HTTPS_PROXY=http://172.30.1.2:8080 \\
  github-gists-api
```

## Verify proxy connectivity first

Run this from the Killercoda terminal:

```bash
curl -v --proxy http://172.30.1.2:8080 https://api.github.com/rate_limit
```

A successful connection should show a successful `CONNECT` tunnel and a GitHub JSON response. If it reports connection refused, timeout, or a tunnel/proxy error, the proxy is not reachable or does not support HTTPS CONNECT. Resolve that before testing the API.

## Verify the API

```bash
curl http://localhost:8080/health
curl http://localhost:8080/octocat
```

Expected health response:

```json
{"status": "ok"}
```

The Gists endpoint returns a JSON array. The application returns `502` if the proxy or GitHub API cannot be reached; it does not intentionally fall back to a direct GitHub connection.

Inspect logs:

```bash
docker compose logs -f
```

Stop the service:

```bash
docker compose down
```

## Run locally without Docker

Python 3.10+ is required:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
HTTPS_PROXY=http://172.30.1.2:8080 python app.py
```

## Automated tests

Tests mock GitHub HTTP responses and do not require a live proxy:

```bash
python -m unittest discover -s tests -v
```

## API

- `GET /<username>` — returns up to 100 public Gists.
- `GET /health` — returns `{"status": "ok"}`.

Errors: `400` invalid GitHub username; `404` GitHub user not found; `502` proxy/network failure or invalid upstream response.

Optionally set `GITHUB_TOKEN` in the environment to authenticate with GitHub and increase the available API rate limit.

## GitHub API reference

[GitHub REST API — List gists for a user](https://docs.github.com/en/rest/gists/gists#list-gists-for-a-user)
