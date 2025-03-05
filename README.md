# Book Library Management System

This project is a **Book Library Management System** built using **FastAPI**, **PostgreSQL**, and **Redis**. It consists of three main services:

1. **Admin API**: For managing books and users.
2. **Frontend API**: For user interactions like borrowing books.
3. **Auth API**: For authentication and authorization.

The system uses **PostgreSQL** as the primary database and **Redis** for caching and message brokering. Authentication in **Frontend API** and **Admin API** is handled by **Auth Service**.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Starting the Services](#starting-the-services)
3. [Service Documentation](#service-documentation)
4. [API Documentation](#api-documentation)
5. [Contributing](#contributing)
6. [License](#license)

## Project Overview

The **Book Library Management System** is designed to handle:

- **Book Management**: Add, remove, and list books.
- **User Management**: Enroll users and manage their profiles.
- **Borrowing System**: Allow users to borrow and return books.
- **Authentication**: Secure access using JWT tokens.

The system is containerized using **Docker** and orchestrated with **Docker Compose**.

## Getting Started

### Prerequisites

- **Docker** and **Docker Compose** installed.
- **Python 3.10** or higher (for local development).

### Starting the Services

1. Clone the repository:

   ```bash
   git clone https://github.com/drlsv91/book-library.git
   cd book-library
   ```

2. Create a `.env` file in the root directory of each service with the required environment variables. Refer to the individual service `README.md` files for details.

3. Start the services using Docker Compose:

   ```bash
   docker-compose up --build
   ```

4. The services will be available at:
   - **Admin API**: `http://localhost:9001`
   - **Frontend API**: `http://localhost:9002`
   - **Auth API**: `http://localhost:9003`
   - **PostgreSQL Database**: `localhost:5432`
   - **Redis**: `localhost:6379`

## Service Documentation

Each service has its own `README.md` file with detailed documentation. Here’s how to access them:

### **Admin API**

- **Path**: `admin_service/README.md`
- **Description**: Manages books and users. Authentication is handled by **Auth service**.
- **Endpoints**: Add/remove books, list users, and more.

### **Frontend API**

- **Path**: `frontend_service/README.md`
- **Description**: Handles user interactions like borrowing books. Authentication is handled by **Auth service**.
- **Endpoints**: Enroll users, list books, borrow books, and more.

### **Auth API**

- **Path**: `auth_service/README.md`
- **Description**: Handles authentication and authorization.
- **Endpoints**: Register users, login, refresh tokens, and more.

## API Documentation

Each service provides API documentation via **Swagger UI** and **ReDoc**:

- **Admin API Docs**: `http://localhost:9001/docs`
- **Frontend API Docs**: `http://localhost:9002/docs`
- **Auth API Docs**: `http://localhost:9003/docs`

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Summary of the Project

The **Book Library Management System** is a scalable and modular application designed to manage books, users, and borrowing operations. It uses modern technologies like **FastAPI**, **PostgreSQL**, and **Redis** to ensure high performance and reliability. The system is containerized using **Docker** for easy deployment and scalability.

This `README.md` file provides a comprehensive guide to setting up, running, and understanding the **Book Library Management System**. For more details, refer to the individual service `README.md` files.

## Running Tests

1. Set the `PYTHONPATH` environment variable:

   ```bash
   export PYTHONPATH=$(pwd)
   ```

2. Use `pytest-watch` to run the tests:

   ```bash
   pytest-watch
   ```
