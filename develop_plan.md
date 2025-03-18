# Mini Habit Tracker with FastAPI, React (Vite + shadcn), PostgreSQL, and MinIO

### Table of Contents

- [Mini Habit Tracker with FastAPI, React (Vite + shadcn), PostgreSQL, and MinIO](#mini-habit-tracker-with-fastapi-react-vite--shadcn-postgresql-and-minio)
  - [Table of Contents](#table-of-contents)
  - [High-Level Overview](#high-level-overview)
  - [Implementation Tools](#implementation-tools)
    - [Frontend](#frontend)
    - [Backend](#backend)
    - [Database](#database)
    - [Object Storage](#object-storage)
  - [MVP Feature Set](#mvp-feature-set)
  - [Database Schema](#database-schema)
    - [1. `users`](#1-users)
    - [2. `habits`](#2-habits)
    - [3. `habit_logs`](#3-habit_logs)
    - [4. _(Optional)_ `files`](#4-optional-files)
  - [FastAPI Endpoints](#fastapi-endpoints)
  - [Frontend Structure](#frontend-structure)
  - [Step-by-Step MVP Plan](#step-by-step-mvp-plan)
  - [Extending with MinIO \& Advanced Use Cases](#extending-with-minio--advanced-use-cases)

---

## High-Level Overview

Create a **habit tracker** that allows users to:

1. **Sign up and authenticate**.
2. **Create and track daily habits**.
3. **Mark habits as done** each day and view minimal stats.

We’ll use:

- **FastAPI** (Python) for the backend.
- **PostgreSQL** for data storage.
- **MinIO** for file/object storage (e.g., storing user profile images, habit-related attachments, etc.).
- **React** (initialized with **Vite**) + **shadcn-ui** for the frontend UI.

---

## Implementation Tools

### Frontend

- **React** + **Vite**
  - Quick build times, modern dev environment.
- **shadcn-ui**
  - A collection of beautiful, pre-built Tailwind CSS components for consistent UI/UX.
- **TypeScript** (optional but recommended) for type safety.

### Backend

- **FastAPI**
  - High-performance Python framework, easy to write clean APIs.
  - Will expose REST endpoints for authentication, habits, logs, and file-upload logic (when using MinIO).

### Database

- **PostgreSQL**
  - Reliable, relational database.
  - Good for production or for more robust local development.

### Object Storage

- **MinIO**
  - S3-compatible, self-hosted object storage solution.
  - Useful for storing **user avatars**, images, or any files you want to attach to habits/logs.
  - For the MVP, you can introduce MinIO in a simple form (e.g., user profile pictures).

---

## MVP Feature Set

1. **User Authentication**

   - Sign Up (username/password)
   - Login (JWT or session token)

2. **Habit Creation & Listing**

   - Create a new habit (name, optional description).
   - View a list of habits belonging to the authenticated user.

3. **Daily Check-In**

   - Mark a habit as done/not done for the day.

4. **Basic Dashboard**

   - Show user’s habits, each with a “Mark Done” button for the current day.
   - Display a minimal statistic, e.g., “X habits done today out of Y.”

5. **(Optional) Light Streak Tracking**
   - Show “current streak” (number of consecutive days completed).

---

## Database Schema

Below is a **more verbose** PostgreSQL schema outline.

### 1. `users`

| Column          | Type           | Constraints                          | Description                                                    |
| --------------- | -------------- | ------------------------------------ | -------------------------------------------------------------- |
| `id`            | `SERIAL`       | `PRIMARY KEY`                        | Unique user identifier.                                        |
| `username`      | `VARCHAR(50)`  | `UNIQUE NOT NULL`                    | User’s unique username.                                        |
| `password_hash` | `VARCHAR(255)` | `NOT NULL`                           | Hashed password (bcrypt, passlib, etc.).                       |
| `avatar_url`    | `TEXT`         | `NULL`                               | (Optional) URL/path to an avatar image stored in MinIO.        |
| `created_at`    | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | When the account was created.                                  |
| `updated_at`    | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Last time this row was updated (can use triggers or manually). |

### 2. `habits`

| Column        | Type           | Constraints                          | Description                                                   |
| ------------- | -------------- | ------------------------------------ | ------------------------------------------------------------- |
| `id`          | `SERIAL`       | `PRIMARY KEY`                        | Unique habit identifier.                                      |
| `user_id`     | `INT`          | `NOT NULL REFERENCES users(id)`      | Owner of this habit.                                          |
| `name`        | `VARCHAR(100)` | `NOT NULL`                           | Habit name.                                                   |
| `description` | `TEXT`         | `NULL`                               | Optional longer description.                                  |
| `created_at`  | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | When this habit was created.                                  |
| `archived_at` | `TIMESTAMP`    | `NULL`                               | If not NULL, the habit is considered “archived” / “inactive.” |

### 3. `habit_logs`

| Column       | Type        | Constraints                          | Description                                           |
| ------------ | ----------- | ------------------------------------ | ----------------------------------------------------- |
| `id`         | `SERIAL`    | `PRIMARY KEY`                        | Unique log identifier.                                |
| `habit_id`   | `INT`       | `NOT NULL REFERENCES habits(id)`     | Links to the habit.                                   |
| `log_date`   | `DATE`      | `NOT NULL`                           | The date of the log (e.g., `2025-03-13`).             |
| `status`     | `BOOLEAN`   | `NOT NULL DEFAULT FALSE`             | Whether the habit was completed (TRUE) or not (FALSE) |
| `created_at` | `TIMESTAMP` | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | When this log was created.                            |

### 4. _(Optional)_ `files`

If you want a separate table to track files stored in MinIO (e.g., user uploads, images for habits, etc.):

| Column        | Type           | Constraints                          | Description                                       |
| ------------- | -------------- | ------------------------------------ | ------------------------------------------------- |
| `id`          | `SERIAL`       | `PRIMARY KEY`                        | Unique file identifier.                           |
| `uploader_id` | `INT`          | `NOT NULL REFERENCES users(id)`      | Who uploaded the file.                            |
| `filename`    | `VARCHAR(255)` | `NOT NULL`                           | Original name of the file.                        |
| `storage_key` | `TEXT`         | `NOT NULL`                           | The key/path used in MinIO (e.g., `bucket/uuid`). |
| `created_at`  | `TIMESTAMP`    | `NOT NULL DEFAULT CURRENT_TIMESTAMP` | Upload date/time.                                 |

> **Note:** For a simple MVP, you might store an `avatar_url` directly on the `users` table. Use MinIO’s S3-like API to upload files and save the returned key in `avatar_url`. A separate `files` table is beneficial if you want to handle multiple files, robust references, or versioning.

---

## FastAPI Endpoints

Here’s a concise but complete set of endpoints for the MVP.

1. **Auth Endpoints**

   - `POST /auth/signup`
     - **Request**: `{"username": "...", "password": "..."}`
     - **Response**: `201 Created` or error
   - `POST /auth/login`
     - **Request**: `{"username": "...", "password": "..."}`
     - **Response**: `{"access_token": "...", "token_type": "bearer"}`

2. **User Profile (Optional)**

   - `GET /users/me`
     - **Response**: Basic user data (including `avatar_url`)
   - `PUT /users/me/avatar` (if implementing file upload)
     - **Request**: multipart/form-data with an image file.
     - **Process**: Upload to MinIO, store the `avatar_url` or `storage_key`.
     - **Response**: Updated user with new avatar URL.

3. **Habit Endpoints**

   - `POST /habits`
     - **Request**: `{"name": "...", "description": "..."}`
     - **Response**: New habit data.
   - `GET /habits`
     - **Response**: List of habits (active) for the user.
   - `DELETE /habits/{habit_id}`
     - Archive or delete habit (for MVP, archiving is optional).

4. **HabitLog Endpoints**
   - `POST /habits/{habit_id}/log`
     - **Request**: `{"log_date": "YYYY-MM-DD", "status": true/false}`
       - Alternatively, assume “today” if not provided.
     - **Response**: New log entry.
   - `GET /habits/{habit_id}/log?start=YYYY-MM-DD&end=YYYY-MM-DD`
     - **Response**: List of log entries for that range (useful for streaks, analytics).

---

## Frontend Structure

1. **Project Bootstrapping**
   - Initialize using **Vite**: `npm create vite@latest my-habit-tracker -- --template react` (or `react-ts`).
   - Install `react-router-dom`, `shadcn-ui` components, and any needed HTTP libraries (axios, fetch).
2. **Key Pages/Routes**

   - **Landing Page** (`/`)

     - Has Header and Footer, describees the features, offers a sign up

   - **Login** (`/login`)
     - Form to submit username/password → receives token → store in local storage or in a secure cookie (simpler for an MVP: local storage).
   - **Signup** (`/signup`)
     - Similar form for new user creation.
   - **Dashboard** (`/dashboard` - protected)
     - Fetch list of habits (`GET /habits`).
     - Display each habit with a simple “Mark as Done” button for the day (`POST /habits/{id}/log`).
   - **Profile** (`/profile` - optional)
     - Show avatar or allow avatar upload (MinIO integration).
   - **Add Habit** (could be a modal or separate route)
     - `POST /habits` with name/description.

3. **UI Components (shadcn-ui)**
   - **Button**, **Input**, **Card**, **Dialog/Modal** for adding habits, **Avatar** if you want to show user profile pictures, etc.
   - Keep the design minimal but cohesive.

---

## Step-by-Step MVP Plan

1. **Set Up FastAPI + PostgreSQL**

   - Create a `main.py` or `app.py` with FastAPI.
   - Install dependencies: `fastapi`, `uvicorn`, `sqlalchemy`, `psycopg2` (for PostgreSQL), etc.
   - Define database models (`users`, `habits`, `habit_logs`).
   - Implement user auth (signup & login).
   - Implement habit creation and listing endpoints.
   - Implement a simple `POST /habits/{id}/log`.

2. **Configure MinIO (Optional for MVP)**

   - Install/Run MinIO locally or on a small container.
   - For the absolute MVP, you can skip file uploads initially.
   - If you do want user avatars:
     - Create an endpoint `PUT /users/me/avatar`.
     - Handle file upload → store in MinIO → record `avatar_url` in `users`.

3. **Set Up React (Vite)**

   - `npm create vite@latest my-habit-tracker -- --template react`
   - Install `react-router-dom`, `shadcn-ui`, `axios`.

4. **Implement Authentication Flow**

   - **Login** page calls `POST /auth/login`, saves the token.
   - **Signup** page calls `POST /auth/signup`.
   - Use a simple private route approach to guard `/dashboard`.

5. **Dashboard & Habits**

   - **Dashboard**:
     - Fetch user’s habits (`GET /habits`).
     - Render each habit, show a “Mark Done” button → calls `POST /habits/{id}/log`.
     - Basic stats: e.g., “X of Y habits done today.”
   - **Add Habit**: A form or modal → `POST /habits`.

6. **(Optional) Streak Logic**

   - On the dashboard, after retrieving logs or daily status, compute consecutive days.
   - Display a simple “Current Streak: N days.”

7. **Testing & Polishing**

   - Test each flow: signup → login → create habit → mark done.
   - Polish the UI with shadcn-ui components for a consistent style.
   - Add small touches: success messages, error handling, etc.

8. **Deployment** (If Desired)
   - **Backend**: Deploy FastAPI + Postgres (Render, Railway, Fly.io).
   - **MinIO**: Deploy on a small VM or container (or switch to AWS S3 if you prefer).
   - **Frontend**: Deploy to Netlify, Vercel, etc.

---

## Extending with MinIO & Advanced Use Cases

Once the MVP is stable, you can add:

1. **Profile Pictures**

   - Users can upload an image. You store it in MinIO under `bucket/username/filename`.
   - Save the resulting path in `avatar_url` on the `users` table.

2. **Habit Attachments**

   - Let users attach images or PDFs to specific habit logs.
   - For instance, “Photo proof of daily run,” or “Screenshot of learning app.”
   - Store references in a `files` table or directly in the `habit_logs`.

3. **Analytics & Charts**

   - Weekly or monthly completion rates.
   - A streak heatmap (like GitHub commits).
   - Leaderboards if you introduce social or team features.

4. **Push Notifications / Reminders**

   - Use Celery or APScheduler to send daily email or push notifications.
   - “Don’t forget to log your habits today!”

5. **Role-Based Access**
   - If you want teams or group features, create different roles and share habits among multiple users.

---
