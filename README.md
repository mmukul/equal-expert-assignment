# GitHub Gists API

A small Flask application that returns the public Gists for a GitHub user.

## Requirements

- Ubuntu or another Linux machine
- Docker
- Docker Compose (`docker-compose`)
- Internet access from the machine to `api.github.com`

## 1. Open the project folder

```bash
cd github-gists-api
```

## 2. Build the application

```bash
docker-compose build
```

## 3. Start the application

```bash
docker-compose up -d
```

## 4. Check that it is running

```bash
docker-compose ps
curl http://localhost:8080/health
```

## 5. Get a user's public Gists

```bash
curl http://localhost:8080/octocat
```

The API returns the user's public Gists as JSON. Replace `octocat` with another GitHub username to retrieve that user's public Gists.

## 6. Run the automated tests

Install the Python packages:

```bash
python3 -m pip install -r requirements.txt
```

Run the tests:

```bash
python3 -m unittest -v
```

