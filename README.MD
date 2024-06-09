# FastAPI JWT Auth

This project is an example of implementing authentication and authorization using FastAPI and JSON Web Tokens (JWT).

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/fastapi-jwt-auth.git
   ```

## Installation with Docker

1. Build the Docker image and start the containers:

   ```bash
   docker-compose up --build
   ```

### Usage

After starting the containers, the server will be available at `http://localhost:8000`.

### Stopping

To stop the containers, run:

```bash
docker-compose down
```

## Local Installation

Create a virtual environment and activate it

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies using poetry

```bash
pip install poetry
poetry install --no-root --no-dev
```

Create a `.env` file in the root directory of the project with the following environment variables:

   ```env
   POSTGRES_PASSWORD=
   POSTGRES_USER=
   POSTGRES_DB=
   PORT=5432
   HOST=localhost
   ```

### Key Pair Generation

To create keys (private and public) in the `certs` folder, run the following commands:

```bash
mkdir certs

openssl genrsa -out certs/jwt-private.pem 2048

openssl rsa -in certs/jwt-private.pem -outform PEM -pubout -out certs/jwt-public.pem
```

### Run Alembic Migrations to Set Up the Database:

```bash
alembic upgrade head
```

## Running

To start the project, run the following command:

```bash
python main.py
```

This will start the FastAPI server at `http://localhost:8000`.

## Usage

The API provides the following endpoints:

- `/auth/register` - Register a new user.
- `/auth/login` - User login.
- `/auth/me` - Get current user information.
- `/auth/logout` - Logout the current user.
- `/auth/refresh-token` - Refresh the JWT token.

To access protected endpoints (e.g., `/auth/me`), you need to provide a JWT token as a cookie named `access_token`.

## Tests

Run tests

```bash
docker-compose -f docker-compose.test.yaml up 
```

## Contribution

If you have suggestions for improving the project, please create a new issue or pull request.

## License

This project is distributed under the MIT License.
