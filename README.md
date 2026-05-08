# Pet Adoption System (Django)

A simple, professionally structured Django project implementing an **MVC-style** architecture with a **Service Layer**.

## Folder structure (key idea)

- **Model**: `adoption/models.py` (Django ORM)
- **Controller**: `adoption/controllers/pet_controller.py` (thin HTTP handlers)
- **Service layer**: `adoption/services/pet_service.py` (business logic)
- **View**: `adoption/templates/adoption/*.html` (Bootstrap UI)

## Prerequisites

- Python 3.11+
- MySQL Server 8.0+
- Git (optional)

## Database Setup

### 1. Install and Configure MySQL

1. Download and install MySQL Server from [mysql.com](https://dev.mysql.com/downloads/mysql/)
2. During installation, set up a root password
3. Start MySQL service

### 2. Create Database User and Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE pet_adoption_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'pet_user'@'localhost' IDENTIFIED BY 'secure_password_123';
GRANT ALL PRIVILEGES ON pet_adoption_db.* TO 'pet_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Import Database Schema and Data

```bash
mysql -u pet_user -p pet_adoption_db < database.sql
```

When prompted, enter the password: `secure_password_123`

### 4. Configure Environment Variables

The `.env` file is already created with default values. For production, update the values in `.env`:

```
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pet_adoption_db
DB_USER=pet_user
DB_PASSWORD=your_secure_password
SECRET_KEY=your_django_secret_key
```

## Setup (Windows PowerShell)

From the folder that contains `manage.py`:

```powershell
cd "c:\Users\Me\Documents\pet_adoption"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.

## Testing Database Connection

After setup, test the database connection:

```powershell
python manage.py shell -c "from django.db import connection; connection.ensure_connection(); print('Database connection successful!')"
```

## API Authentication

This project includes JWT-based authentication similar to Laravel Sanctum. All API endpoints require authentication except registration and login.

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

#### Login User
```http
POST /api/auth/login/
Content-Type: application/json

{
  "username": "johndoe",
  "password": "securepassword123"
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
  "refresh": "your_refresh_token_here"
}
```

#### Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer your_access_token_here
```

### Using API Tokens

Include the access token in the `Authorization` header for all authenticated requests:

```
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### Pet API Endpoints

#### Get All Pets
```http
GET /api/pets/
Authorization: Bearer your_token
```

#### Get Pet Details
```http
GET /api/pets/{id}/
Authorization: Bearer your_token
```

#### Create Pet
```http
POST /api/pets/create/
Authorization: Bearer your_token
Content-Type: application/json

{
  "name": "Buddy",
  "species": "Dog",
  "breed": "Golden Retriever",
  "age": 3,
  "description": "Friendly dog",  // optional
  "status": "available",          // optional, defaults to "available"
  "image": "https://example.com/buddy.jpg"  // optional
}
```

**Note:** `description` and `image` are optional fields. If not provided or empty, they will be set to `null` in the database. The `status` field defaults to `"available"` if not specified.

#### Update Pet
```http
PUT /api/pets/{id}/update/
Authorization: Bearer your_token
Content-Type: application/json

{
  "name": "Buddy Updated",
  "status": "adopted"
}
```

**Note:** All fields are optional in update requests. Only provided fields will be updated. `description` and `image` can be set to `null` by providing empty strings or omitting them.

#### Delete Pet
```http
DELETE /api/pets/{id}/delete/
Authorization: Bearer your_token
```

#### Adopt Pet
```http
POST /api/pets/{id}/adopt/
Authorization: Bearer your_token
Content-Type: application/json

{
  "adopter_name": "John Doe",
  "adopter_email": "john@example.com"
}
```

## Testing Authentication

Run the included test script to verify authentication works:

```bash
python test_auth.py
```

This will:
- Register a test user
- Login and get JWT tokens
- Test authenticated API endpoints
- Create, read, and update pets

## Features

- View list of available pets
- View pet details
- Add / Edit / Delete a pet
- Submit adoption request (marks pet as **adopted**)
- View adoption success message

## Security Notes

- Never commit `.env` file to version control
- Use strong passwords for database users
- Generate a new SECRET_KEY for production
- Set DEBUG=False in production

