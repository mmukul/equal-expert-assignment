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
docker compose up --build
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
sudo apt update
sudo apt install python3-full python3-venv python3-pip -y
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

```
python3 -m unittest -v
```
