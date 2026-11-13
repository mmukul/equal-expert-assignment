# GitHub Gists API

A small Flask application that returns the public Gists for a GitHub user.

## Requirements

- Rocky Linux machine
- Docker
- Docker Compose

## 1. Open the project folder

```bash
cd equal-expert-assignment
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
```

```
curl http://localhost:8080/health
```

## 5. Get a user's public Gists

```bash
curl http://localhost:8080/octocat
```

## 6. Run the automated tests

```bash
python3 -m pip install -r requirements.txt
```

```
python3 -m unittest -v
```
