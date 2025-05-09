# Admin Service (Book Library Management System)

The **Admin Service** is responsible for managing books and users in the Book Library Management System.

## Requirements

- [Docker](https://www.docker.com/).
- [uv](https://docs.astral.sh/uv/) for Python package and environment management.

## Endpoints

- `POST /books/`: add a new book.
- `GET /books/`: Retrieve books.
- `DELETE /books/{book_id}`: Retrieve book by ID.
- `GET /users/`: Retrieve users.
- `GET /users/books`: Retrieve users' books.

---

## Technology Stack and Features

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the Python backend API.

  - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the Python SQL database interactions (ORM).
  - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
  - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.

- 🐋 [Docker Compose](https://www.docker.com) for development and production.
- 🔒 Secure password hashing by default.
- 🔑 JWT (JSON Web Token) authentication.
- ✅ Tests with [Pytest](https://pytest.org).

### Configure

You can update configs in the `.env` files to customize your configurations.

Before deploying it, make sure you change at least the values for:

- `SECRET_KEY`
- `POSTGRES_PASSWORD`

## Port

- **Port**: `9001`

---

## Dependencies

- **PostgreSQL**: For storing user data.
- **Redis**: For caching or message brokering.

---

## Running the Service

1. Ensure Docker and Docker Compose are installed.
2. Navigate to the project root directory.
3. Run the following command:
   ```bash
   docker-compose up --build
   ```
