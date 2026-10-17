# MealsRater API

A RESTful API built with Django and Django REST Framework that lets users browse meals and rate them from 1 to 5 stars. Each meal shows its number of ratings and its average rating.

## Features

- User registration with token-based authentication
- CRUD operations for meals (authenticated users only)
- Custom endpoint to create or update a rating for a meal
- One rating per user per meal (enforced by a database unique constraint)
- Rating validation (1-5 stars)
- Each user can only see and delete their own ratings
- Secrets loaded from environment variables
- Automated API tests

## Tech Stack

- Python
- Django
- Django REST Framework (Token Authentication)
- SQLite
- python-decouple

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/kareemkeshta98-hue/MealsRater-API.git
cd MealsRater-API
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and set your own secret key:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
```

To generate a secret key:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Run migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/API/`.

## Running Tests

```bash
python manage.py test
```

## API Endpoints

| Method | Endpoint | Description | Auth required |
|--------|----------|-------------|---------------|
| POST | `/API/users/` | Register a user and get a token | No |
| GET | `/API/meals/` | List all meals | Yes |
| POST | `/API/meals/` | Create a meal | Yes |
| GET | `/API/meals/{id}/` | Get a single meal | Yes |
| POST | `/API/meals/{id}/rate_meal/` | Rate a meal (creates or updates) | Yes |
| GET | `/API/ratings/` | List your own ratings | Yes |

Authenticated requests need this header:

```
Authorization: Token <your-token>
```

## Example Usage

**Register a user**

```http
POST /API/users/
Content-Type: application/json

{"username": "test1", "password": "your-password"}
```

Response:

```json
{"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
```

**Rate a meal**

```http
POST /API/meals/1/rate_meal/
Authorization: Token <your-token>
Content-Type: application/json

{"stars": 4}
```

Response (`201 Created` on first rating, `200 OK` on update):

```json
{
    "message": "Meal Rate Created",
    "result": {"id": 1, "stars": 4, "user": 1, "meal": 1}
}
```

Invalid or missing `stars` returns `400 Bad Request`.

## Possible Improvements

- Add pagination and search for meals
- Deploy online