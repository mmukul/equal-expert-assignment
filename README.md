# GitHub Public Gists API Assignment

A small Flask API that returns the public Gists for a GitHub username.

- API address: `http://localhost:8080`
- External HTTP proxy: `http://172.30.1.2:8080`
- Proxy authentication: not required
- API container port: `8080`

## 1. Fix the proxy first

The API health endpoint is working, but the GitHub request currently fails.
The proxy test returned:

```text
HTTP/1.1 405 METHOD NOT ALLOWED
Server: Werkzeug
Allow: OPTIONS, GET, HEAD
```

This means the service at `172.30.1.2:8080` is responding like a normal Flask
web application. It is not accepting the HTTPS `CONNECT` method required by
an HTTP forward proxy.

The following setup assumes you have administrator access to `172.30.1.2`.
Run these commands on the proxy machine, not inside the API container.

### Install Squid

```bash
sudo apt update
sudo apt install squid -y
```

Check whether another service is using port `8080`:

```bash
sudo ss -ltnp | grep ':8080'
```

Squid needs port `8080` to be free. If another application is using it, stop
or reconfigure that application only after confirming what it does.

### Restrict proxy access to the API machine

Find the source IP address of the machine running the API. On the proxy
machine, you can watch the Squid access log while testing:

```bash
sudo tail -f /var/log/squid/access.log
```

Edit the Squid configuration:

```bash
sudo nano /etc/squid/squid.conf
```

Use this minimal configuration, replacing `API_CLIENT_IP` with the real
source IP address of the API machine:

```conf
http_port 8080

acl api_client src API_CLIENT_IP/32
acl SSL_ports port 443
acl Safe_ports port 80 443
acl CONNECT method CONNECT

http_access deny !Safe_ports
http_access deny CONNECT !SSL_ports
http_access allow api_client
http_access deny all
```

For example, use `172.30.1.10/32` only if `172.30.1.10` is actually the API
machine's source IP. Do not guess the address. This rule allows only that
machine to use the proxy and avoids creating an unrestricted open proxy.

Validate and restart Squid:

```bash
sudo squid -k parse
sudo systemctl restart squid
sudo systemctl enable squid
sudo systemctl status squid
```

If Squid does not start, check the logs:

```bash
sudo journalctl -u squid --no-pager -n 50
```

## 2. Test the proxy

Run this on the machine where the API will run:

```bash
curl -v --proxy http://172.30.1.2:8080 \
  https://api.github.com/rate_limit
```

A successful test shows `200 Connection established` for the HTTPS tunnel
and then prints JSON from GitHub.

If the result is:
- `405`: the service on port `8080` is still not accepting proxy CONNECT.
- `403`: check the API machine IP in the Squid access rule.
- Connection refused or timeout: check Squid status, firewall and network access.

Do not continue to the API test until this proxy test succeeds.

## 3. Build and start the API

From the project directory, run:

```bash
docker-compose up --build -d
```

This command works with Docker Compose `1.29.2`. If you install Compose v2,
you can instead use `docker compose up --build -d`.

The proxy is configured in `docker-compose.yml` as:

```yaml
HTTPS_PROXY: http://172.30.1.2:8080
```

The API container listens on port `8080`. The proxy uses the same port on a
different IP address, so the ports do not conflict.

Check the container and logs:

```bash
docker ps
docker-compose logs -f
```

## 4. Test the API

Check that the API is running:

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

A successful request returns a JSON array. The API returns `502` if the
proxy or GitHub API cannot be reached.

Stop the application:

```bash
docker-compose down
```

## 5. Run automated tests

The tests mock GitHub responses, so they do not need a live proxy or internet:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

## API endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Check API health |
| GET | `/<username>` | Return up to 100 public Gists |
