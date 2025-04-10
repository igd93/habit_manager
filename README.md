# Habit Tracker Application

[![CI](https://github.com/clockiz/productivity/actions/workflows/ci.yml/badge.svg)](https://github.com/clockiz/productivity/actions/workflows/ci.yml)

A full-stack habit tracking application with a React frontend and FastAPI backend.

## Tech Stack

### Frontend

- React (with Vite)
- TypeScript
- Shadcn UI (Tailwind CSS components)
- React Router

### Backend

- FastAPI
- PostgreSQL
- SQLAlchemy ORM
- MinIO (S3-compatible object storage)
- Alembic (database migrations)

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Node.js (for local frontend development)
- Python 3.11+ (for local backend development)

### Running with Docker Compose

The easiest way to run the entire application is using Docker Compose:

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

This will start:

- PostgreSQL database
- MinIO object storage
- FastAPI backend
- React frontend

### Services & Ports

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Backend API Documentation: http://localhost:8000/docs
- MinIO Console: http://localhost:9001 (login: minioadmin/minioadmin)
- PostgreSQL: localhost:5432 (credentials in docker-compose.yml)

## Project Structure

```
/
├── frontend/           # React frontend
│   ├── src/            # Frontend source code
│   └── Dockerfile      # Frontend Docker configuration
│
├── backend/            # FastAPI backend
│   ├── app/            # Backend source code
│   ├── alembic/        # Database migrations
│   └── Dockerfile      # Backend Docker configuration
│
└── docker-compose.yml  # Docker services configuration
```

## Features

- User authentication
- Create and manage habits
- Track daily habit completion
- View progress statistics
- User profile with avatar (stored in MinIO)

## Contributing

1. Clone the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Make your changes
4. Submit a pull request
