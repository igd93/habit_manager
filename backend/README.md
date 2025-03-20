# Habit Tracker API

This is the FastAPI backend for the Habit Tracker application.

## Tech Stack

- **FastAPI**: Modern, fast API framework
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **PostgreSQL**: Relational database
- **MinIO**: S3-compatible object storage
- **Poetry**: Dependency management

## Development Setup

### Using Docker Compose

The easiest way to run the backend is with Docker Compose. From the root directory:

```bash
docker-compose up -d
```

This will start the backend along with PostgreSQL and MinIO.

### Manual Setup

1. Install dependencies using Poetry:

```bash
cd backend
poetry install
```

2. Create a `.env` file (copy from `.env.example` and update as needed)

3. Run the development server:

```bash
poetry run uvicorn app.main:app --reload
```

## Database Migrations

To create a new migration after modifying models:

```bash
# Inside the backend container
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head
```

## API Documentation

When the server is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
