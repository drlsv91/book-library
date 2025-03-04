# Admin Service (Book Library Management System)

The **Admin Service** is responsible for managing books and users in the Book Library Management System.

---

## Endpoints

- `POST /books/`: Add a new book.
- `DELETE /books/{book_id}`: Remove a book.
- `GET /users/`: List all users.
- `GET /borrowed-books/`: List all borrowed books.
- `GET /unavailable-books/`: List all unavailable books.

---

## Port

- **Port**: `9001`

---

## Dependencies

- **PostgreSQL**: For storing books, users, and borrowed books.
- **Redis**: For caching or message brokering.

---

## Running the Service

1. Ensure Docker and Docker Compose are installed.
2. Navigate to the project root directory.
3. Run the following command:
   ```bash
   docker-compose up --build
   ```
