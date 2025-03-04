---
# Frontend Service (API Book Library Management System)

The **Frontend Service** handles user interactions such as enrolling users, listing books, and borrowing books.
---

## Endpoints

- `POST /users/`: Enroll a new user.
- `GET /books/`: List all available books.
- `GET /books/{book_id}`: Get a single book by ID.
- `GET /books/filter/`: Filter books by publisher or category.
- `POST /books/borrow/`: Borrow a book.

---

## Port

- **Port**: `9002`

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
