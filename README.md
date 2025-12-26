## Overview

This is a Django REST API for a mobile app that allows users to review places (shops, doctors, restaurants, etc.).
It implements user registration/login, adding reviews, searching for places, and viewing place details, along with a data
population command for testing.

## Assumptions

- **Authentication**: Although the problem statement only mentions name and phone number, a password is also required
  for secure login. Users register with `name`, `phone`, and `password`.
- **Category**: The statement mentions "If a category is entered". A `category` field is added on `Place` with choices:
  `shop`, `doctor`, `restaurant`, `other`. It is optional when adding a review.
- **Database**: Uses SQLite (relational) by default for simplicity; this can be switched to any relational database in
  `reviews_api/settings.py`.
- **Auth Mechanism**: Uses Django REST Framework Token Authentication (no external services).

## How to run

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Apply migrations**

   ```bash
   python manage.py migrate
   ```

3. **(Optional) Create a superuser**

   ```bash
   python manage.py createsuperuser --phone 9999999999 --name "Admin User"
   ```

4. **Populate sample data**

   ```bash
   python manage.py seed_data
   ```

5. **Run the development server**

   ```bash
   python manage.py runserver
   ```

## API Endpoints

All endpoints require authentication **except** registration and login. Authentication is via token in the `Authorization` header:

`Authorization: Token <token>`

- **Register**
  - `POST /api/auth/register/`
  - Body: `{ "name": "...", "phone": "9000000000", "password": "secret123" }`
  - Response: user data (without password).

- **Login**
  - `POST /api/auth/login/`
  - Body: `{ "phone": "9000000000", "password": "secret123" }`
  - Response: `{ "token": "<token>" }`

- **Add Review**
  - `POST /api/reviews/add/`
  - Body:
    ```json
    {
      "place_name": "Star Cafe",
      "place_address": "MG Road, Bangalore",
      "rating": 5,
      "text": "Great place",
      "category": "restaurant"
    }
    ```
  - If a place with the same name and address exists, the review is added to it; otherwise a new place is created.

- **Search Places**
  - `GET /api/places/search/?name=<name>&min_rating=<float>&category=<category>`
  - Name filter:
    - Exact-name matches appear first.
    - Partial matches (substring, case-insensitive) appear after exact matches.
  - Rating filter:
    - `min_rating` filters by **average** rating (across all reviews) greater than or equal to the value.
  - Category filter:
    - If `category` is provided, only places of that category are considered.
  - Response: list of places with fields: `id`, `name`, `address`, `category`, `average_rating`.

- **Place Details**
  - `GET /api/places/<id>/`
  - Response: `name`, `address`, `category`, `average_rating`, and all reviews.
  - Review ordering:
    - If the current user has left a review, their review(s) appear at the top.
    - All other reviews follow, sorted by newest first.

## Data Population

The `seed_data` management command creates:
- 10 users with phone numbers `9000000000` to `9000000009`, password `password123`.
- A handful of places with different categories.
- A random set of reviews from the users for those places.

Run:

```bash
python manage.py seed_data
```


