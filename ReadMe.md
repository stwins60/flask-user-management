# Flask User Management API

## Overview
This project is a Flask-based microservice for user management, featuring user registration, authentication via JWT, and profile retrieval. The application uses PostgreSQL as the database backend and provides API documentation via Swagger.

## Features
- User registration with hashed passwords.
- User login with JWT authentication.
- Profile retrieval endpoint.
- PostgreSQL database integration.
- API documentation via Swagger.

## Technologies Used
- Python 3
- Flask
- Flask-JWT-Extended
- Flask-SQLAlchemy
- PostgreSQL
- Docker
- Swagger for API documentation
- dotenv for environment variable management

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.8+
- PostgreSQL

### Steps

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the environment variables by creating a `.env` file:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/userdb
   JWT_SECRET_KEY=your_secret_key
   ```

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the Flask application:
   ```bash
   python app.py
   ```

7. Access the application at `http://localhost:5000`

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t flask-user-management .
   ```

2. Run the container:
   ```bash
   docker run -p 5000:5000 --env-file .env flask-user-management
   ```

## API Endpoints

| Method | Endpoint    | Description               |
|--------|------------|---------------------------|
| POST   | /register   | Register a new user       |
| POST   | /login      | Login and get JWT token   |
| GET    | /profile    | Get user profile (auth required) |

## Accessing Swagger Docs
Swagger UI can be accessed at:
```
http://localhost:5000/api/docs
```

## Testing
Run unit tests using:
```bash
pytest
```

## License
This project is licensed under the MIT License.

