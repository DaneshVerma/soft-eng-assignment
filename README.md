# User Management API

## Project Overview
This project is a professional, production-ready Flask application designed to manage user records. It provides a RESTful API for creating, retrieving, searching, and paginating user data. The architecture follows a clean modular design with separate layers for routing, business logic (services), and data access (models), ensuring extensibility and maintainability.

## Technology Stack
- **Framework**: Flask
- **Language**: Python 3.12+
- **Database**: MySQL (supported via PyMySQL), configured to use SQLite by default for local development fallback.
- **ORM**: SQLAlchemy (Flask-SQLAlchemy)
- **Migrations**: Alembic (Flask-Migrate)
- **Testing**: Pytest
- **Environment Management**: python-dotenv

## Project Structure
```text
app/
├── errors.py           # Centralized error handling
├── extensions.py       # Flask extensions initialization
├── config.py           # Environment-based configuration
├── __init__.py         # Application factory
├── models/
│   ├── user.py         # SQLAlchemy models
├── routes/
│   ├── user_routes.py  # API route definitions
├── services/
│   ├── user_service.py # Business logic layer
├── utils/
│   ├── validation.py   # Input validation logic
tests/                  # Automated API tests using pytest
migrations/             # Alembic database migrations
run.py                  # Application entry point
requirements.txt        # Python dependencies
pytest.ini              # Pytest configuration
.env.example            # Example environment variables
```

## Setup Instructions

1. Clone the repository and navigate into the directory.
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # Unix/MacOS
   source .venv/bin/activate
   ```
   *(Alternatively, if using `uv`: `uv venv`)*
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Variables

Copy the example environment file and update it with your own credentials:
```bash
cp .env.example .env
```
Ensure the `DATABASE_URL` is configured to point to your MySQL or SQLite instance.

## Database Setup & Migration Commands

To initialize the database and apply the latest schema changes, run:
```bash
# Apply existing migrations
flask db upgrade
```

To create a new migration after modifying models:
```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

## Running the Application

### Using Docker (Recommended)
To start the application and the MySQL database in isolated containers, use Docker Compose:
```bash
docker compose up -d --build
```
This automatically runs database migrations and maps the API to `http://127.0.0.1:5000`.

### Local Development Server
To start the development server natively (requires setting up your own database):
```bash
python run.py
```
The application will run on `http://127.0.0.1:5000`.

## Testing

To execute the automated API tests, run:
```bash
pytest
```
The test suite utilizes an isolated in-memory SQLite database to ensure the development database remains unaffected.

---

## API Documentation

### 1. Create a User
- **Endpoint**: `POST /users`
- **Description**: Creates a new user in the system.
- **Example Request**:
  ```json
  POST /users
  Content-Type: application/json

  {
      "name": "John Doe",
      "email": "john.doe@example.com",
      "role": "admin"
  }
  ```
- **Example Response** (201 Created):
  ```json
  {
      "success": true,
      "data": {
          "id": 1,
          "name": "John Doe",
          "email": "john.doe@example.com",
          "role": "admin",
          "created_at": "2026-08-04T12:00:00.000000",
          "updated_at": "2026-08-04T12:00:00.000000"
      }
  }
  ```

### 2. Get Users (with Pagination & Search)
- **Endpoint**: `GET /users`
- **Description**: Retrieves a paginated list of users. Supports searching by name or email.
- **Query Parameters**:
  - `page` (optional): Page number (default: 1)
  - `limit` (optional): Items per page (default: 10)
  - `search` (optional): Search term for filtering by name or email (case-insensitive)
- **Example Request**:
  ```
  GET /users?page=1&limit=2&search=john
  ```
- **Example Response** (200 OK):
  ```json
  {
      "success": true,
      "page": 1,
      "limit": 2,
      "total": 1,
      "total_pages": 1,
      "data": [
          {
              "id": 1,
              "name": "John Doe",
              "email": "john.doe@example.com",
              "role": "admin",
              "created_at": "...",
              "updated_at": "..."
          }
      ]
  }
  ```

### 3. Get User by ID
- **Endpoint**: `GET /users/<id>`
- **Description**: Retrieves a specific user by their unique ID.
- **Example Request**:
  ```
  GET /users/1
  ```
- **Example Response** (200 OK):
  ```json
  {
      "success": true,
      "data": {
          "id": 1,
          "name": "John Doe",
          "email": "john.doe@example.com",
          "role": "admin",
          "created_at": "...",
          "updated_at": "..."
      }
  }
  ```
- **Error Response** (404 Not Found):
  ```json
  {
      "success": false,
      "error": "User not found"
  }
  ```

---

## Database Schema

**Table: `users`**
| Column       | Type         | Constraints                                |
|--------------|--------------|--------------------------------------------|
| `id`         | Integer      | Primary Key, Auto-increment                |
| `name`       | String(100)  | Not Null                                   |
| `email`      | String(120)  | Not Null, Unique                           |
| `role`       | String(50)   | Not Null                                   |
| `created_at` | DateTime     | Not Null, Default: Current UTC timestamp   |
| `updated_at` | DateTime     | Not Null, Default/On Update: UTC timestamp |

---

## Assumptions Made
- The application focuses strictly on a standard REST API response format (`success` and `data`/`error` keys).
- For local execution without an active MySQL server, a SQLite fallback (`sqlite:///app.db`) is configured to ensure seamless developer onboarding and immediate runnable state.
- Authentication (like JWT) is intentionally excluded per project constraints, prioritizing robust basic validation and structure over access control.
- Pagination is implemented using offset/limit mechanics standard to SQLAlchemy, which is suitable for standard traffic expectations.

## AI Usage Declaration

**AI Tools Used**: Google Deepmind's Agentic AI Assistant
**What AI Generated**: The entirety of the codebase was scaffolded and implemented by AI following constraints provided via prompts. This includes the application factory setup, model configuration, service/route separation, validation logic, Pytest cases, centralized error handlers, and this README documentation.
**What was Manually Modified**: The AI acted autonomously to create the code. Explicit design requirements, architecture constraints, and testing criteria were specified by the developer to guide the AI's generation.

---

## Assignment Questions

### 1. Why Flask?
Flask is a lightweight, extensible micro-framework perfectly suited for building microservices or tightly-scoped APIs. Unlike Django, which is heavily opinionated and comes with built-in monolithic structures, Flask allows developers to adopt a modular "Application Factory" pattern with explicitly defined service layers. This minimizes boilerplate while providing the flexibility to plug in precisely the extensions needed (like SQLAlchemy and Flask-Migrate).

### 2. How would this scale?
- **Statelessness**: The API is currently entirely stateless. It can easily be scaled horizontally behind a load balancer (e.g., NGINX, AWS ALB) by spawning multiple identical containers or worker processes.
- **Database Scaling**: As the `users` table grows, the `email` and `name` columns will require indexing to keep `ILIKE` or `LIKE` searches performant. Eventually, full-text search (like Elasticsearch) or caching layers (like Redis) could be introduced to offload complex queries from the primary SQL database.
- **Pagination**: The current offset-based pagination could become slow on extremely large datasets. It would be migrated to cursor-based pagination (keyset pagination) for better scaling on deep pages.

### 3. Production improvements?
- **Dockerization (Completed)**: The application has successfully been wrapped in a `Dockerfile` and orchestrated via Docker Compose, fulfilling the initial need for containerization and environment parity. Next steps would involve Kubernetes for larger scale.
- **Server Infrastructure**: The built-in Flask server is not designed for production traffic. A robust WSGI server like `Gunicorn` (with `gevent` or threaded workers) managed by a reverse proxy (`NGINX`) must be used.
- **Security**: Integrating authentication (JWT/OAuth), rate limiting (e.g., Flask-Limiter), and robust CORS headers are vital production necessities.
- **Observability**: Adding structured logging, Prometheus metrics, and APM tracing (like DataDog or Sentry) is required to monitor exceptions and endpoint performance in real-time.
- **Database Migrations**: In production, migrations should be strictly automated as part of a CI/CD pipeline, avoiding manual `flask db upgrade` execution.
