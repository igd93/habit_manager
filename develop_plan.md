# Mini Habit Tracker with FastAPI, React (Vite + shadcn), PostgreSQL, and MinIO

## Table of Contents

- [High-Level Overview](#high-level-overview)
- [Implementation Tools](#implementation-tools)
- [MVP Feature Set](#mvp-feature-set)
- [Database Schema](#database-schema)
- [FastAPI Endpoints](#fastapi-endpoints)
- [Frontend Structure](#frontend-structure)
- [Implementation Plan](#implementation-plan)
- [Future Enhancements](#future-enhancements)

## High-Level Overview

Create a **habit tracker** that allows users to:

1. **Sign up and authenticate**
2. **Create and track daily habits**
3. **Mark habits as done** each day
4. **View minimal stats** on habit completion

### Tech Stack

- **Frontend**: React (Vite) + shadcn-ui
- **Backend**: FastAPI (Python)
- **Database**: PostgreSQL
- **Object Storage**: MinIO (for user avatars and attachments)

## Implementation Tools

### Frontend

- **React + Vite**: Modern, fast React setup with quick build times
- **shadcn-ui**: Beautiful, consistent UI components based on Tailwind CSS
- **TypeScript**: Type safety for improved developer experience
- **React Router**: For page navigation and protected routes

### Backend

- **FastAPI**: High-performance Python API framework with automatic docs
- **SQLAlchemy**: SQL toolkit and ORM for database interactions
- **Pydantic**: Data validation and settings management
- **Python-jose**: JWT token handling for authentication

### Database

- **PostgreSQL**: Reliable, relational database system
- **Alembic**: Database migration tool

### Object Storage

- **MinIO**: S3-compatible object storage for storing user avatars and attachments
- **Python client**: For interacting with MinIO from the backend

## MVP Feature Set

1. **User Authentication**

   - Sign up with username/password
   - Login with JWT token
   - Protected routes

2. **Habit Management**

   - Create new habits with name and description
   - View list of current habits
   - Archive/delete habits (optional for MVP)

3. **Daily Check-In**

   - Mark habits as completed for the day
   - Simple UI for quick habit tracking

4. **Basic Dashboard**
   - Overview of habits with completion status
   - Simple stat: "X of Y habits completed today"
   - Current streak tracking (optional)

## Database Schema

### 1. `users` Table

| Column          | Type           | Constraints                          | Description                        |
| --------------- | -------------- | ------------------------------------ | ---------------------------------- |
| `id`            | `SERIAL`       | `PRIMARY KEY`                        | Unique user identifier             |
| `username`      | `VARCHAR(50)`  | `UNIQUE NOT NULL`                    | User's unique username             |
| `password_hash` | `VARCHAR(255)` | `NOT NULL`                           | Securely hashed password           |
| `avatar_url`    | `TEXT`         | `NULL`                               | Path to avatar in MinIO (optional) |
| `created_at`    | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Account creation timestamp         |
| `updated_at`    | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Last update timestamp              |

### 2. `habits` Table

| Column        | Type           | Constraints                          | Description                    |
| ------------- | -------------- | ------------------------------------ | ------------------------------ |
| `id`          | `SERIAL`       | `PRIMARY KEY`                        | Unique habit identifier        |
| `user_id`     | `INT`          | `NOT NULL REFERENCES users(id)`      | Owner of the habit             |
| `name`        | `VARCHAR(100)` | `NOT NULL`                           | Habit name                     |
| `description` | `TEXT`         | `NULL`                               | Optional habit description     |
| `created_at`  | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | When habit was created         |
| `archived_at` | `TIMESTAMP`    | `NULL`                               | If not NULL, habit is archived |

### 3. `habit_logs` Table

| Column       | Type        | Constraints                          | Description                 |
| ------------ | ----------- | ------------------------------------ | --------------------------- |
| `id`         | `SERIAL`    | `PRIMARY KEY`                        | Unique log identifier       |
| `habit_id`   | `INT`       | `NOT NULL REFERENCES habits(id)`     | Reference to the habit      |
| `log_date`   | `DATE`      | `NOT NULL`                           | Date of the log entry       |
| `status`     | `BOOLEAN`   | `NOT NULL DEFAULT FALSE`             | Whether habit was completed |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | When log was created        |

### 4. `files` Table (Optional)

| Column        | Type           | Constraints                          | Description                         |
| ------------- | -------------- | ------------------------------------ | ----------------------------------- |
| `id`          | `SERIAL`       | `PRIMARY KEY`                        | Unique file identifier              |
| `uploader_id` | `INT`          | `NOT NULL REFERENCES users(id)`      | User who uploaded the file          |
| `filename`    | `VARCHAR(255)` | `NOT NULL`                           | Original filename                   |
| `storage_key` | `TEXT`         | `NOT NULL`                           | Path in MinIO (e.g., `bucket/uuid`) |
| `created_at`  | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Upload timestamp                    |

## FastAPI Endpoints

### Authentication

- `POST /auth/signup`

  - Request: `{"username": "user1", "password": "securepass"}`
  - Response: `201 Created` or error

- `POST /auth/login`
  - Request: `{"username": "user1", "password": "securepass"}`
  - Response: `{"access_token": "eyJh...", "token_type": "bearer"}`

### User Profile

- `GET /users/me`

  - Response: User details including `avatar_url`

- `PUT /users/me/avatar` (Optional)
  - Request: `multipart/form-data` with image file
  - Response: Updated user with new avatar URL

### Habits

- `POST /habits`

  - Request: `{"name": "Read daily", "description": "20 minutes of reading"}`
  - Response: New habit data

- `GET /habits`

  - Response: List of active habits for authenticated user

- `DELETE /habits/{habit_id}`
  - Response: Success or error message

### Habit Logs

- `POST /habits/{habit_id}/log`

  - Request: `{"log_date": "2023-06-15", "status": true}`
  - Response: Created log entry

- `GET /habits/{habit_id}/log?start=YYYY-MM-DD&end=YYYY-MM-DD`
  - Response: List of log entries for date range

## Frontend Structure

### Pages

1. **Landing Page** (`/`)

   - Marketing content, features overview
   - Links to login/signup

2. **Auth Pages**

   - **Login** (`/login`)
     - Username/password form
     - JWT token storage in localStorage
   - **Signup** (`/signup`)
     - Registration form with validation

3. **Dashboard** (`/dashboard`)

   - Protected route requiring authentication
   - Habit listing with completion status
   - Summary statistics

4. **Add Habit** (`/habits/new`)

   - Form to create new habits
   - Name & description fields

5. **Profile** (`/profile`) (Optional)
   - User details
   - Avatar upload using MinIO

### Components

1. **Layout Components**

   - `Header`: Navigation and user status
   - `Footer`: App links and info
   - `MainLayout`: Page structure container

2. **UI Components**

   - `HabitCard`: Display habit with actions
   - `CompletionStat`: Show progress statistics
   - `HabitForm`: Create/edit habits

3. **Auth Components**
   - `ProtectedRoute`: Route guard for authentication
   - `AuthContext`: User auth state management

## Implementation Plan

### 1. Project Setup & Auth

- [x] Initialize React (Vite) frontend
- [x] Set up shadcn-ui components
- [x] Create landing page with auth links
- [x] Implement login & signup pages
- [ ] Create FastAPI project structure
- [ ] Set up PostgreSQL database
- [ ] Implement user model and auth endpoints

### 2. Core Habit Functionality

- [ ] Create database models for habits and logs
- [ ] Implement habit CRUD API endpoints
- [ ] Develop dashboard UI for habits list
- [ ] Add habit creation form
- [ ] Implement habit completion functionality

### 3. Stats & Polish

- [ ] Add basic completion statistics
- [ ] Implement streak tracking (optional)
- [ ] Improve UI/UX with loading states and feedback
- [ ] Add error handling and validation

### 4. MinIO Integration (Optional)

- [ ] Set up MinIO server
- [ ] Create user avatar upload feature
- [ ] Implement avatar display in UI

### 5. Testing & Deployment

- [ ] Test authentication flows
- [ ] Verify habit tracking functionality
- [ ] Ensure responsive design works
- [ ] Deploy backend and frontend

## Future Enhancements

1. **Profile Customization**

   - Profile pictures via MinIO
   - User settings and preferences

2. **Habit Attachments**

   - Attach images or files to habit logs
   - Visual evidence of habit completion

3. **Advanced Analytics**

   - Completion rate charts
   - Streak heatmaps
   - Progress trends

4. **Notifications & Reminders**

   - Email or push notifications
   - Daily habit reminders

5. **Social Features**
   - Shared habits between users
   - Teams and accountability groups
