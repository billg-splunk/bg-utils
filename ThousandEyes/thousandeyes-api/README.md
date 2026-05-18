# ThousandEyes User API

A small Flask service that exposes a simple HTTP endpoint to create users in ThousandEyes via the [ThousandEyes Administrative API v7](https://developer.cisco.com/docs/thousandeyes/create-user/).

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Health check |
| `GET` | `/showinfo` | List valid values for optional `.env` settings |
| `GET` | `/adduser?email=...` | Create a user in ThousandEyes |

### Discover configuration values

Uses your `THOUSANDEYES_API_TOKEN` to query ThousandEyes for account groups, roles, and related IDs you can copy into `.env`:

```bash
curl "http://localhost:8080/showinfo" | python3 -m json.tool > output.json
```

The response includes:

- **`current_config`** — what is set in the environment now (token shown as `configured`, not the secret)
- **`settings`** — per-variable descriptions, suggested values, and `options` lists with `value` / `label` pairs
- **`hints`** — default and current account group metadata
- **`users_sample`** — up to five users (if your token has permission), useful for seeing `loginAccountGroup` examples
- **`errors`** — partial failures (e.g. roles or users forbidden) without failing the whole request
- **`suggested_value`** - provides recommendations on what value to use

Any time you change `.env` you will need to restart the application/docker containers.

### Create a user

```bash
curl "http://localhost:8080/adduser?email=bob@company.com"
```

Optional query parameter:

- `name` — display name (defaults to the part before `@` in the email)

Example with a custom name:

```bash
curl "http://localhost:8080/adduser?email=bob@company.com&name=Bob%20Smith"
```

On success, the service returns HTTP `201` with the user object from ThousandEyes.

## Prerequisites

- Docker (recommended) or Python 3.12+
- A ThousandEyes [user API token](https://docs.thousandeyes.com/product-documentation/user-management/rbac#user-api-tokens) with permission to create users
- Your user role must include API access (Organization Admin, Account Admin, and Regular User include this by default)

## Configuration

Copy the example environment file and fill in your values:

```bash
cp .env.example .env
```

| Variable | Required | Description |
|----------|----------|-------------|
| `THOUSANDEYES_API_TOKEN` | Yes | Bearer token from Account Settings → Users and Roles → Profile |
| `THOUSANDEYES_ACCOUNT_GROUP_ID` | No | Account group ID (`aid` query parameter) when operating in a specific account group |
| `THOUSANDEYES_DEFAULT_ROLE_IDS` | No | Comma-separated role IDs assigned to new users (e.g. Regular User role ID) |
| `THOUSANDEYES_LOGIN_ACCOUNT_GROUP_ID` | No | Login account group ID for the new user |

The API token is read only from the environment and is never stored in source code.

Use **`GET /showinfo`** after setting the token to discover valid IDs for the optional variables above.

## Run with Docker Compose

```bash
cp .env.example .env
# Edit .env and set THOUSANDEYES_API_TOKEN (and other vars as needed)

docker compose up --build
```

The service listens on port **8080**.

`docker compose build` only builds the image; it does **not** start the server. You must run `docker compose up` (or `docker compose up -d` to run in the background).

Verify the container is running:

```bash
docker compose ps
curl http://localhost:8080/health
```

Expected health response: `{"status":"ok"}`

To stop: `docker compose down`

## Run with Docker (without Compose)

```bash
docker build -t thousandeyes-api .
docker run --rm -p 8080:8080 --env-file .env thousandeyes-api
```

## Run locally (without Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

export THOUSANDEYES_API_TOKEN=your-token-here
# Optional:
# export THOUSANDEYES_ACCOUNT_GROUP_ID=1234
# export THOUSANDEYES_DEFAULT_ROLE_IDS=57
# export THOUSANDEYES_LOGIN_ACCOUNT_GROUP_ID=691

gunicorn --bind 0.0.0.0:8080 wsgi:app
```

## Project layout

```
.
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes.py            # /adduser, /showinfo, and /health endpoints
│   └── thousandeyes_client.py
├── wsgi.py                  # Gunicorn entrypoint
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── README.md
```

## ThousandEyes API details

This service calls:

- **POST** `https://api.thousandeyes.com/v7/users`
- **Authentication:** `Authorization: Bearer <token>`

See the [Create user API reference](https://developer.cisco.com/docs/thousandeyes/create-user/) for full request/response schemas and error codes.

## Error responses

| HTTP status | Meaning |
|-------------|---------|
| `400` | Missing or invalid `email` query parameter |
| `201` | User created successfully |
| `4xx` / `5xx` | ThousandEyes API error (details included in response body) |
| `500` | Missing `THOUSANDEYES_API_TOKEN` or other server configuration error |
