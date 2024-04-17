# painel-carreiras-api

## Overview
Painel de Carreiras is a web application designed to offer users detailed insights into various career paths, including salary distributions, job postings, positions available, and more. Built with FastAPI, the application provides a robust API and an interactive client interface, making it easier for users to navigate and extract meaningful career-related information.

## Features
- **Dynamic Job Postings**: Browse and search through listings of job postings, filtering by position, location, and company.
- **Salary Insights**: Access detailed salary distribution data for different positions, helping users understand potential earnings in their field.
- **Secure User Authentication**: Manage user sessions securely with login and logout capabilities.
- **Interactive Dashboards**: Visualize data through charts and tables directly on the platform, offering a user-friendly experience for data interaction.

## Technologies
- **FastAPI**: Utilizes FastAPI for backend operations, providing a high-performance API.
- **Alembic**: Handles database migrations, ensuring that the database schema is up to date with the application's requirements.
- **Poetry**: Manages dependencies and packages, facilitating consistent development and deployment environments.
- **Docker**: Simplifies deployment and enhances scalability through containerization of the application.
- **htmx**: Enhances the front-end with AJAX capabilities, enabling dynamic content updates without needing to reload the page.
- **Jinja2**: Serves as the template engine for rendering HTML, providing a powerful tool for generating dynamic web pages.
- **Chart.js**: Integrates graphical data presentations on the frontend, making statistical data comprehensible and visually appealing.

## Folder structure

```yml
.
├── Dockerfile                        # Dockerfile for building the application container.
├── README.md                         # Project README providing information and instructions.
├── docker-compose.yml                # Docker Compose file for defining and running multi-container Docker applications.
├── mypy.ini                          # Configuration file for MyPy, a static type checker.
├── poetry.lock                       # Poetry lock file specifying exact versions of dependencies to ensure consistent environments.
├── pyproject.toml                    # Configuration file for Poetry that includes project metadata and dependencies.
│
├── src                               # Source code directory.
│   ├── __init__.py                   # Initialization file for the src package.
│   ├── alembic.ini                   # Configuration file for Alembic to manage database migrations.
│   │
│   ├── app                           # Main application directory.
│   │   ├── __init__.py               # Initialization file for the app package.
│   │   ├── main.py                   # Main entry point for the FastAPI application.
│   │   │
│   │   ├── api                       # Folder containing API-related logic.
│   │   │   ├── dependencies.py       # Defines dependencies used across API endpoints.
│   │   │   │
│   │   │   └── v1                    # Version 1 of the API.
│   │   │       ├── login.py          # API route for user login.
│   │   │       ├── logout.py         # API route for user logout.
│   │   │       ├── users.py          # API routes for user management.
│   │   │       └── rate_limits.py    # API routes for rate limiting functionalities.
│   │   │
│   │   ├── client                    # Client-specific components of the application.
│   │   │   ├── dashboard.py          # Logic for the dashboard page.
│   │   │   ├── landing.py            # Logic for the landing page.
│   │   │   ├── login.py              # Logic for the login page.
│   │   │   ├── positions.py          # Logic for the positions page.
│   │   │   └── postings.py           # Logic for the job postings page.
│   │   │
│   │   ├── core                      # Core utilities and configurations for the application.
│   │   │   ├── config.py             # Application configuration settings.
│   │   │   ├── security.py           # Security utilities, such as password hashing.
│   │   │   ├── setup.py              # Setup file for initializing the FastAPI app instance.
│   │   │   └── db                    # Database related modules.
│   │   │       ├── database.py       # Database connectivity and session management.
│   │   │       └── models.py         # Database models.
│   │   │
│   │   ├── crud                      # CRUD operations for the application.
│   │   │   └── crud_users.py         # CRUD operations for users.
│   │   │
│   │   └── templates                 # HTML templates used by the application.
│   │       ├── base.html             # Base template for common layout of all pages.
│   │       ├── dashboard.html        # Template for the dashboard page.
│   │       ├── landing.html          # Template for the landing page.
│   │       ├── login_page.html       # Template for the login page.
│   │       ├── positions.html        # Template for the positions page.
│   │       ├── positions_table.html  # Template for the positions table.
│   │       ├── postings.html         # Template for the job postings page.
│   │       └── postings_table.html   # Template for the job postings table.
│   │
│   └── migrations                    # Alembic migration scripts for database schema changes.
│       └── env.py                    # Environment configuration for Alembic.
│
└── tests                             # Unit and integration tests for the application.
    └── __init__.py                   # Initialization file for the test package.
```

## Start

Start by cloning the repository.

```sh
git clone https://github.com/DataCraft-Labs/painel-carreiras-api
```

## Environment Variables (.env)

Then create a `.env` file inside `src` directory:

```sh
touch .env
```

Inside of `.env`, create the following app settings variables:

```
# ------------- app settings -------------
APP_NAME="Your app name here"
APP_DESCRIPTION="Your app description here"
APP_VERSION="0.1"
CONTACT_NAME="Your name"
CONTACT_EMAIL="Your email"
LICENSE_NAME="The license you picked"
```

For the database ([`if you don't have a database yet, click here`](#422-running-postgresql-with-docker)), create:

```
# ------------- database -------------
POSTGRES_USER="your_postgres_user"
POSTGRES_PASSWORD="your_password"
POSTGRES_SERVER="your_server" # default "localhost", if using docker compose you should use "db"
POSTGRES_PORT=5432 # default "5432", if using docker compose you should use "5432"
POSTGRES_DB="your_db"
```

For database administration using PGAdmin create the following variables in the .env file

```
# ------------- pgadmin -------------
PGADMIN_DEFAULT_EMAIL="your_email_address"
PGADMIN_DEFAULT_PASSWORD="your_password"
PGADMIN_LISTEN_PORT=80
```

To connect to the database, log into the PGAdmin console with the values specified in `PGADMIN_DEFAULT_EMAIL` and `PGADMIN_DEFAULT_PASSWORD`.

Once in the main PGAdmin screen, click Add Server:

![pgadmin-connect](https://github.com/igorbenav/docs-images/blob/main/289698727-e15693b6-fae9-4ec6-a597-e70ab6f44133-3.png?raw=true)

1. Hostname/address is `db` (if using containers)
1. Is the value you specified in `POSTGRES_PORT`
1. Leave this value as `postgres`
1. is the value you specified in `POSTGRES_USER`
1. Is the value you specified in `POSTGRES_PASSWORD`

For crypt:
Start by running

```sh
openssl rand -hex 32
```

And then create in `.env`:

```
# ------------- crypt -------------
SECRET_KEY= # result of openssl rand -hex 32
ALGORITHM= # pick an algorithm, default HS256
ACCESS_TOKEN_EXPIRE_MINUTES= # minutes until token expires, default 30
REFRESH_TOKEN_EXPIRE_DAYS= # days until token expires, default 7
```

Then for the first admin user:

```
# ------------- admin -------------
ADMIN_NAME="your_name"
ADMIN_EMAIL="your_email"
ADMIN_USERNAME="your_username"
ADMIN_PASSWORD="your_password"
```

For redis caching:

```
# ------------- redis cache-------------
REDIS_CACHE_HOST="your_host" # default "localhost", if using docker compose you should use "redis"
REDIS_CACHE_PORT=6379 # default "6379", if using docker compose you should use "6379"
```

And for client-side caching:

```
# ------------- redis client-side cache -------------
CLIENT_CACHE_MAX_AGE=30 # default "30"
```

For ARQ Job Queues:

```
# ------------- redis queue -------------
REDIS_QUEUE_HOST="your_host" # default "localhost", if using docker compose you should use "redis"
REDIS_QUEUE_PORT=6379 # default "6379", if using docker compose you should use "6379"
```

> \[!WARNING\]
> You may use the same redis for both caching and queue while developing, but the recommendation is using two separate containers for production.

To create the first tier:

```
# ------------- first tier -------------
TIER_NAME="free"
```

For the rate limiter:

```
# ------------- redis rate limit -------------
REDIS_RATE_LIMIT_HOST="localhost"   # default="localhost", if using docker compose you should use "redis"
REDIS_RATE_LIMIT_PORT=6379          # default=6379, if using docker compose you should use "6379"


# ------------- default rate limit settings -------------
DEFAULT_RATE_LIMIT_LIMIT=10         # default=10
DEFAULT_RATE_LIMIT_PERIOD=3600      # default=3600
```

For tests (optional to run):

```
# ------------- test -------------
TEST_NAME="Tester User"
TEST_EMAIL="test@tester.com"
TEST_USERNAME="testeruser"
TEST_PASSWORD="Str1ng$t"
```

And Finally the environment:

```
# ------------- environment -------------
ENVIRONMENT="local"
```

`ENVIRONMENT` can be one of `local`, `staging` and `production`, defaults to local, and changes the behavior of api `docs` endpoints:

- **local:** `/docs`, `/redoc` and `/openapi.json` available
- **staging:** `/docs`, `/redoc` and `/openapi.json` available for superusers
- **production:** `/docs`, `/redoc` and `/openapi.json` not available

## Running

In the root directory, run:

```sh
docker compose up
```

Then head to `http://127.0.0.1:8000/` to access the app or `http://127.0.0.1:8000/docs` to get swagger.
