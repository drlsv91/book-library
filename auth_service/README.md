---
# User Service

The **User Service** handles user authentication and authorization.
---

## Endpoints

- `POST /register/`: Register a new user.
- `POST /login/`: Authenticate a user and generate a JWT token.
- `POST /refresh-token/`: Refresh an expired JWT token.
- `GET /me/`: Get the current user's profile.

---

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
