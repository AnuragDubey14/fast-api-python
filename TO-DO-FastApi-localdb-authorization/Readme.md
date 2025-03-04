# FastAPI To-Do App with Local Database and Authorization

This project is a robust To-Do application built with FastAPI. It leverages SQLAlchemy for persistent storage, Pydantic for data validation, and JWT for secure user authentication. The application features a clean and modular architecture with comprehensive endpoints for creating, reading, updating, and deleting tasks—all while ensuring that only authorized users can manage their tasks.

## Features

- **JWT-Based Authentication:** 
  Secure user registration and login with JSON Web Tokens to protect endpoints.

- **Local Database Authorization:**  
  Each task is linked to a specific user, ensuring that only the owner can view, update, or delete their tasks.

- **CRUD Operations:**  
  Endpoints to create, retrieve, update, and delete to-do items.

- **Data Validation:**  
  Pydantic models enforce data integrity and automatically generate API documentation.

- **Asynchronous Endpoints:**  
  Built on FastAPI’s asynchronous framework for efficient request handling.

- **Comprehensive Testing:**  
  Extensive test cases built with pytest and FastAPI’s TestClient to ensure endpoint reliability.

- **Clean & Modular Architecture:**  
  Clearly separated modules for routes, models, and schemas to support scalability and future enhancements.

## Technologies Used

- **FastAPI** – A modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **SQLAlchemy** – An SQL toolkit and ORM for Python to manage database interactions.
- **Pydantic** – Data validation and settings management using Python type annotations.
- **JWT** – JSON Web Tokens for secure authentication.
- **MySQL** – Relational database for persistent storage.
- **Pytest** – Testing framework for Python.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/AnuragDubey14/fast-api-python.git
   cd fast-api-python/TO-DO-FastApi-localdb-authorization
   ```


2. **Activate a Virtual Environment:**

   ```bash
   # On Windows:
   fastenv\Scripts\activate
   # On macOS/Linux:
   source fastenv/bin/activate
   ```


3. **Configure Environment Variables:**

   Create a `.env` file (if required) to store your configuration such as:
   - `DB_URL=mysql+pymysql://<username>:<password>@<host>:<port>/<database>`
   - `SECRET_KEY=your_secret_key`
   - (Other configurations as needed)

4. **Set Up the Database:**

   Ensure you have a MySQL database created (e.g., `to_do_fast` for production or a dedicated test database).

5. **Run the Application:**

   ```bash
   fastapi dev app.py
   ```

   The server should start at [http://127.0.0.1:8000](http://127.0.0.1:8000). Swagger UI documentation is available at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

- **User Registration:**  
  `POST /register` – Register a new user.

- **User Login:**  
  `POST /token` – Log in to obtain a JWT token.

- **Task Operations:**  
  - `GET /tasks` – Retrieve all tasks for the authenticated user.  
  - `GET /task/` – Retrieve a specific task by ID or title.  
  - `POST /task/` – Add a new task (requires authentication).  
  - `PUT /task/` – Update an existing task (requires authentication).  
  - `PATCH /task/status` – Update task status.  
  - `PATCH /task/deadline` – Update task deadline.  
  - `DELETE /task/` – Delete a task (requires authentication).

## Testing

Tests are written using pytest and FastAPI’s TestClient. To run the tests:

1. **Configure a Test Database(in MySQL):**  
   ```bash
   CREATE DATABASE test_db
   ```

2. **Run Pytest:**

   ```bash
   pytest test.py
   ```

   This will run all test cases and provide a summary.

## Future Enhancements

- Expand error handling and logging.
- Implement additional features such as task categorization, deadlines reminders, etc.
- Enhance security with more granular permission controls.
- Containerize the application using Docker.

## Contributing

Contributions, suggestions, and feedback are welcome! Feel free to open issues or submit pull requests.

---

