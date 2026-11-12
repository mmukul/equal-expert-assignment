# GitHub Gists API

A small Flask API that returns a GitHub user's public Gists.

## 1. Requirements

- Docker
- Docker Compose (the `docker-compose` command)
- A working HTTP proxy that supports HTTPS `CONNECT`

## 2. Project files

- `app.py` — API
- `requirements.txt` — Python packages
- `Dockerfile` — container build
- `docker-compose.yml` — container settings and proxy
- `README.md` — instructions

## 3. Build and start

Run these commands from this project folder:

```bash
docker-compose build
docker-compose up -d
docker-compose ps
```

## 4. Test the API

Check that the application is running:

```bash
curl http://localhost:8080/health
```

Expected response:

```json
{"status":"ok"}
```

Get the public Gists for `octocat`:

```bash
curl http://localhost:8080/octocat
```

The response should be a JSON array.

## 5. Run the automated tests

Install the Python packages on the machine where you are running the tests:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest -v
```

The tests check the health endpoint, a successful Gists response, and a GitHub user-not-found response. They use mocked GitHub responses, so they do not need a working internet connection or proxy.

## 6. Stop the application

```bash
docker-compose down
```

## Proxy note

The Compose file points to `http://172.30.1.2:8080`.

That address must be a real forward proxy that supports HTTPS `CONNECT`. A normal web server is not sufficient. If the proxy returns `405 Method Not Allowed` for a `CONNECT` request, the proxy is not configured for HTTPS tunnelling and the Gists request will fail.

To test the proxy from the host:

```bash
curl -v --proxy http://172.30.1.2:8080 https://api.github.com/rate_limit
```

A working proxy should establish the tunnel and then return GitHub JSON. If your proxy uses a different address or port, update `HTTPS_PROXY` in `docker-compose.yml` and rebuild/restart:

```bash
docker-compose down
docker-compose up -d --build
```
