# README - Backend (Flask)

## Online Gallery Platform - Backend

This is the backend part of Artistry, a web application built with Flask. The backend handles authentication, image management, and user data.

---

## Installation and Setup

### Requirements:

- Python (v3.8 or later)
- pip (Python package manager)

### Installation

1. Navigate to the backend folder:

   ```sh
   cd artistry-backend
   ```

2. Create a virtual environment (recommended):

   ```sh
   python -m venv venv
   ```

3. Activate the virtual environment:

   - **Windows**:
     ```sh
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```sh
     source venv/bin/activate
     ```

4. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

5. Start the server:

   ```sh
   python run.py
   ```

   The server will run on [http://localhost:5000](http://localhost:5000).

---

## Database Structure

The backend uses SQLite (for development) and includes the following tables:

### User Table

- `id` (Integer, primary key)
- `username` (String, unique)
- `email` (String, unique)
- `password_hash` (String)
- `created_at` (DateTime)

### Artwork Table

- `id` (Integer, primary key)
- `title` (String)
- `description` (Text)
- `image_path` (String)
- `created_at` (DateTime)
- `user_id` (Foreign Key -> User.id)

---

## PR Rules

- All Pull Requests must be reviewed by at least one other team member.
- Code should follow the project's style guide.
- Clear commit messages describing the changes are required.

---

## Known Bugs / Upcoming Features

- Add a commenting feature for artworks.
- Expand user profiles with more details.
- Implement social sharing features.
