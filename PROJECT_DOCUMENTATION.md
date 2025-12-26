# Places Review API - Complete Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Project Architecture](#project-architecture)
4. [File Structure & Explanation](#file-structure--explanation)
5. [Database Schema](#database-schema)
6. [API Endpoints & Flow](#api-endpoints--flow)
7. [Key Features & Implementation Details](#key-features--implementation-details)
8. [Authentication Flow](#authentication-flow)
9. [How to Run](#how-to-run)

---

## 🎯 Project Overview

This is a **Django REST API** for a mobile application that allows users to review places (shops, doctors, restaurants, etc.). The API provides endpoints for:

- **User Management**: Registration and authentication using phone numbers
- **Place Management**: Creating and searching places
- **Review System**: Adding reviews with ratings (1-5) and text
- **Search Functionality**: Search places by name, minimum rating, and category with intelligent ordering

### What Problem Does It Solve?

The API serves as the backend for a mobile app where users can:
- Register and authenticate securely
- Leave reviews for any place (restaurants, shops, doctors, etc.)
- Search for places based on various criteria
- View detailed information about places including all reviews

---

## 🛠 Technology Stack

### Core Technologies
- **Python 3.x**: Programming language
- **Django 6.0**: High-level Python web framework
- **Django REST Framework 3.16.1**: Toolkit for building REST APIs
- **SQLite**: Relational database (can be switched to PostgreSQL/MySQL)

### Key Libraries & Features Used
- **Django ORM**: Database abstraction layer
- **Token Authentication**: REST Framework's token-based authentication
- **Django Migrations**: Database schema version control
- **Custom User Model**: Phone-based authentication
- **Custom Authentication Backend**: Phone number as username

### Why These Technologies?
- **Django**: Robust, secure, and follows best practices
- **Django REST Framework**: Simplifies API development with serializers, viewsets, and authentication
- **SQLite**: Easy to set up, perfect for development (can switch to PostgreSQL for production)
- **Token Authentication**: Stateless, simple, and works well for mobile apps

---

## 🏗 Project Architecture

### MVC-like Pattern (Django's MVT)
- **Models** (`models.py`): Database schema and business logic
- **Views** (`views.py`): Request handlers (API endpoints)
- **Serializers** (`serializers.py`): Data validation and transformation
- **URLs** (`urls.py`): URL routing

### Request Flow
```
Client Request → URLs (routing) → Views (business logic) → Serializers (validation) → Models (database) → Response
```

---

## 📁 File Structure & Explanation

### Root Directory Files

#### `manage.py`
**Purpose**: Django's command-line utility for administrative tasks
**What it does**:
- Entry point for Django commands (migrate, runserver, createsuperuser, etc.)
- Sets up Django environment and imports settings
- Example commands: `python manage.py migrate`, `python manage.py runserver`

#### `requirements.txt`
**Purpose**: Lists all Python package dependencies
**Contents**:
```
django==6.0
djangorestframework==3.16.1
```
**Why**: Ensures anyone can install exact same dependencies

#### `db.sqlite3`
**Purpose**: SQLite database file (created after migrations)
**What it contains**: All tables (users, places, reviews) and data
**Note**: This is the actual database - don't delete it unless you want to lose data

#### `README.md`
**Purpose**: Quick start guide and API documentation
**Contains**: Installation steps, API endpoint documentation, assumptions

#### `test_api.py`
**Purpose**: Comprehensive test script for API endpoints
**What it does**:
- Tests all endpoints (register, login, add review, search, place details)
- Tests authentication requirements
- Can be run independently: `python test_api.py`
- Useful for manual testing and verification

---

### `reviews_api/` Directory (Django Project Configuration)

This is the main Django project folder that contains configuration files.

#### `reviews_api/settings.py`
**Purpose**: Main configuration file for the Django project
**Key Configurations**:

1. **Database Settings** (lines 80-85):
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.sqlite3',
           'NAME': BASE_DIR / 'db.sqlite3',
       }
   }
   ```
   - Configures SQLite database
   - Can be changed to PostgreSQL/MySQL for production

2. **Custom User Model** (line 87):
   ```python
   AUTH_USER_MODEL = 'reviews.User'
   ```
   - Tells Django to use our custom User model instead of default

3. **Authentication Backends** (lines 89-92):
   ```python
   AUTHENTICATION_BACKENDS = [
       'reviews.backends.PhoneAuthBackend',
       'django.contrib.auth.backends.ModelBackend',
   ]
   ```
   - Custom backend allows login with phone number
   - Fallback to default backend for admin

4. **REST Framework Settings** (lines 94-101):
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_AUTHENTICATION_CLASSES': [
           'rest_framework.authentication.TokenAuthentication',
       ],
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.IsAuthenticated',
       ],
   }
   ```
   - Token authentication for API
   - All endpoints require authentication by default

5. **Installed Apps** (lines 33-45):
   - Lists all Django apps used in the project
   - Includes Django admin, auth, and our `reviews` app

#### `reviews_api/urls.py`
**Purpose**: Main URL routing configuration (root URLconf)
**What it does**:
- Maps URLs to view functions/classes
- Includes admin URLs
- Routes API endpoints:
  - `/api/auth/register/` → RegisterView
  - `/api/auth/login/` → LoginView
  - `/api/reviews/add/` → AddReviewView
  - `/api/places/search/` → SearchPlacesView
  - `/api/places/<id>/` → PlaceDetailView

**URL Pattern Example**:
```python
path("api/auth/register/", review_views.RegisterView.as_view(), name="register")
```
- `api/auth/register/` is the URL path
- `RegisterView.as_view()` is the view that handles the request
- `name="register"` allows reverse URL lookup

#### `reviews_api/wsgi.py`
**Purpose**: WSGI (Web Server Gateway Interface) configuration
**What it does**: Used for deploying to production servers (like Apache, Nginx)
**Note**: Not used in development, but required for production deployment

#### `reviews_api/asgi.py`
**Purpose**: ASGI (Asynchronous Server Gateway Interface) configuration
**What it does**: Used for async web servers and WebSocket support
**Note**: Not used in this project, but included by default

#### `reviews_api/__init__.py`
**Purpose**: Makes the directory a Python package
**What it does**: Empty file that tells Python this folder is a package

---

### `reviews/` Directory (Main Application)

This is the Django app that contains all the business logic.

#### `reviews/models.py`
**Purpose**: Defines database models (tables) and their relationships
**Contains Three Models**:

1. **User Model** (lines 29-49):
   ```python
   class User(AbstractBaseUser, PermissionsMixin):
       name = models.CharField(max_length=255)
       phone = models.CharField(max_length=20, unique=True)
   ```
   - Custom user model (replaces Django's default)
   - Uses phone number as unique identifier (not email)
   - `unique=True` ensures only one user per phone number
   - Inherits from `AbstractBaseUser` for authentication features

2. **Place Model** (lines 52-75):
   ```python
   class Place(models.Model):
       name = models.CharField(max_length=255)
       address = models.TextField()
       category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
       
       class Meta:
           constraints = [
               models.UniqueConstraint(
                   fields=["name", "address"],
                   name="unique_place_name_address",
               )
           ]
   ```
   - Represents a physical location (restaurant, shop, etc.)
   - `UniqueConstraint` ensures same name+address can't exist twice
   - Category field with choices: shop, doctor, restaurant, other

3. **Review Model** (lines 78-94):
   ```python
   class Review(models.Model):
       place = models.ForeignKey(Place, on_delete=models.CASCADE)
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
       text = models.TextField(blank=True)
       created_at = models.DateTimeField(auto_now_add=True)
   ```
   - Links a user's review to a place
   - `ForeignKey`: Many reviews can belong to one place/user
   - `CASCADE`: If place/user deleted, reviews are deleted too
   - Rating validation: Only 1-5 allowed
   - `auto_now_add=True`: Automatically sets timestamp on creation

**Why Models Matter**: They define the database structure. Django automatically creates SQL tables from these models.

#### `reviews/serializers.py`
**Purpose**: Converts between Python objects and JSON (and validates data)
**Contains Five Serializers**:

1. **UserRegisterSerializer** (lines 7-17):
   - Validates registration data (name, phone, password)
   - Creates new user with hashed password
   - Returns user data (without password)

2. **LoginSerializer** (lines 20-31):
   - Validates phone and password
   - Authenticates user using custom backend
   - Returns user object if valid

3. **PlaceSerializer** (lines 34-42):
   - Serializes Place objects for search results
   - Includes calculated `average_rating` field
   - Returns: id, name, address, category, average_rating

4. **ReviewSerializer** (lines 45-50):
   - Serializes Review objects
   - Includes `user_name` (from related user)
   - Returns: id, rating, text, user_name, created_at

5. **PlaceDetailSerializer** (lines 53-62):
   - Serializes Place with all reviews
   - Used for place detail endpoint
   - Returns: id, name, address, category, average_rating, reviews[]

6. **AddReviewSerializer** (lines 65-72):
   - Validates review creation data
   - Ensures rating is 1-5
   - Validates category if provided

**Why Serializers Matter**: They handle data validation, transformation, and ensure API responses are consistent.

#### `reviews/views.py`
**Purpose**: Contains API endpoint handlers (business logic)
**Contains Five View Classes**:

1. **RegisterView** (lines 18-20):
   ```python
   class RegisterView(generics.CreateAPIView):
       serializer_class = UserRegisterSerializer
       permission_classes = [permissions.AllowAny]
   ```
   - Handles `POST /api/auth/register/`
   - Allows anyone to register (no auth required)
   - Uses UserRegisterSerializer to create user

2. **LoginView** (lines 23-31):
   ```python
   class LoginView(APIView):
       def post(self, request):
           # Authenticates user and returns token
   ```
   - Handles `POST /api/auth/login/`
   - Authenticates user, creates/returns token
   - Token used for subsequent API calls

3. **AddReviewView** (lines 34-60):
   ```python
   def post(self, request):
       place, created = Place.objects.get_or_create(
           name=data["place_name"].strip(),
           address=data["place_address"].strip(),
       )
       review = Review.objects.create(...)
   ```
   - Handles `POST /api/reviews/add/`
   - **Key Logic**: `get_or_create()` - creates place if doesn't exist
   - Creates review linked to place and current user
   - Requires authentication (inherited from settings)

4. **SearchPlacesView** (lines 63-98):
   ```python
   def get_queryset(self):
       queryset = Place.objects.all().annotate(
           average_rating=Avg("reviews__rating")
       )
       # Filter by name, min_rating, category
       # Order: exact matches first, then by name
   ```
   - Handles `GET /api/places/search/`
   - **Key Features**:
     - Calculates average rating using `Avg()` aggregation
     - Filters by name (partial match, case-insensitive)
     - Filters by minimum rating
     - Filters by category
     - **Smart Ordering**: Exact name matches first, then partial matches
   - Uses Django ORM annotations for efficient queries

5. **PlaceDetailView** (lines 101-117):
   ```python
   def retrieve(self, request, *args, **kwargs):
       # Get place
       # Order reviews: user's reviews first, then newest first
   ```
   - Handles `GET /api/places/<id>/`
   - **Key Logic**: Custom review ordering
     - Current user's reviews appear first
     - Other reviews sorted by newest first
   - Returns place details with all reviews

**Why Views Matter**: They contain the actual business logic and handle HTTP requests/responses.

#### `reviews/backends.py`
**Purpose**: Custom authentication backend for phone-based login
**What it does**:
```python
class PhoneAuthBackend(ModelBackend):
    def authenticate(self, request, phone=None, password=None, **kwargs):
        user = User.objects.get(phone=phone)
        if user.check_password(password):
            return user
```
- Allows users to login with phone number (instead of username)
- Checks password against hashed password in database
- Required because Django's default uses username/email

**Why It's Needed**: Django's default authentication uses username, but we use phone numbers.

#### `reviews/admin.py`
**Purpose**: Django admin interface configuration
**What it does**: Registers models so they appear in Django admin panel
**Note**: Can be used to manage data through web interface at `/admin/`

#### `reviews/apps.py`
**Purpose**: App configuration
**What it does**: Contains metadata about the app
**Note**: Usually left as default, but can customize app behavior here

#### `reviews/__init__.py`
**Purpose**: Makes directory a Python package
**What it does**: Empty file, required for Python imports

#### `reviews/tests.py`
**Purpose**: Unit tests for the app
**What it does**: Currently empty, but should contain test cases
**Note**: Django's testing framework would go here

#### `reviews/migrations/0001_initial.py`
**Purpose**: Database migration file
**What it does**: 
- Created automatically by Django when you run `python manage.py makemigrations`
- Contains SQL commands to create tables
- Applied to database with `python manage.py migrate`
- **Never edit manually** - Django generates these

#### `reviews/management/commands/seed_data.py`
**Purpose**: Custom Django management command to populate database with sample data
**What it does**:
```python
class Command(BaseCommand):
    def handle(self, *args, **options):
        # Creates 10 users
        # Creates 5 places
        # Creates random reviews
```
- Can be run with: `python manage.py seed_data`
- Creates test data for development/testing
- Uses `get_or_create()` to avoid duplicates on re-run

**Why It's Useful**: Quickly populates database for testing without manual data entry.

---

## 🗄 Database Schema

### Entity Relationship Diagram
```
User (1) ────< (Many) Review (Many) >─── (1) Place
```

### Tables

#### `reviews_user`
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String(255) | Not Null |
| phone | String(20) | Unique, Not Null |
| password | String | Hashed |
| is_active | Boolean | Default True |
| date_joined | DateTime | Auto |

#### `reviews_place`
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| name | String(255) | Not Null |
| address | Text | Not Null |
| category | String(20) | Default 'other' |
| **Unique Constraint**: (name, address) |

#### `reviews_review`
| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| place_id | Integer | Foreign Key → Place |
| user_id | Integer | Foreign Key → User |
| rating | Integer | 1-5 (validated) |
| text | Text | Optional |
| created_at | DateTime | Auto |

---

## 🔌 API Endpoints & Flow

### 1. User Registration
**Endpoint**: `POST /api/auth/register/`
**Flow**:
```
Client → RegisterView → UserRegisterSerializer → User.objects.create_user() → Database
                                                      ↓
                                                  Response (user data)
```

**Request**:
```json
{
  "name": "John Doe",
  "phone": "9000000000",
  "password": "secret123"
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "name": "John Doe",
  "phone": "9000000000"
}
```

### 2. User Login
**Endpoint**: `POST /api/auth/login/`
**Flow**:
```
Client → LoginView → LoginSerializer → PhoneAuthBackend.authenticate() → Token.objects.get_or_create() → Response
```

**Request**:
```json
{
  "phone": "9000000000",
  "password": "secret123"
}
```

**Response**: `200 OK`
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### 3. Add Review
**Endpoint**: `POST /api/reviews/add/`
**Headers**: `Authorization: Token <token>`
**Flow**:
```
Client → AddReviewView → AddReviewSerializer → Place.objects.get_or_create() → Review.objects.create() → Response
```

**Request**:
```json
{
  "place_name": "Star Cafe",
  "place_address": "MG Road, Bangalore",
  "rating": 5,
  "text": "Great food!",
  "category": "restaurant"
}
```

**Key Logic**: 
- If place exists (same name+address), adds review to it
- If place doesn't exist, creates new place first, then adds review

**Response**: `201 Created`
```json
{
  "id": 1,
  "rating": 5,
  "text": "Great food!",
  "user_name": "John Doe",
  "created_at": "2024-01-15T10:30:00Z"
}
```

### 4. Search Places
**Endpoint**: `GET /api/places/search/?name=Star&min_rating=4.0&category=restaurant`
**Headers**: `Authorization: Token <token>`
**Flow**:
```
Client → SearchPlacesView → get_queryset() → Database Query (with filters) → PlaceSerializer → Response
```

**Query Parameters**:
- `name`: Partial match, case-insensitive
- `min_rating`: Filter by average rating >= value
- `category`: Filter by category

**Ordering Logic**:
1. Exact name matches first (using `Case/When` annotation)
2. Partial matches second
3. Within each group, sorted alphabetically by name

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "Star Cafe",
    "address": "MG Road, Bangalore",
    "category": "restaurant",
    "average_rating": 4.5
  }
]
```

### 5. Place Details
**Endpoint**: `GET /api/places/<id>/`
**Headers**: `Authorization: Token <token>`
**Flow**:
```
Client → PlaceDetailView → retrieve() → Get Place → Order Reviews → PlaceDetailSerializer → Response
```

**Review Ordering Logic**:
1. Current user's reviews first (if any)
2. All other reviews, sorted by newest first

**Response**: `200 OK`
```json
{
  "id": 1,
  "name": "Star Cafe",
  "address": "MG Road, Bangalore",
  "category": "restaurant",
  "average_rating": 4.5,
  "reviews": [
    {
      "id": 5,
      "rating": 5,
      "text": "My review",
      "user_name": "John Doe",
      "created_at": "2024-01-15T10:30:00Z"
    },
    {
      "id": 3,
      "rating": 4,
      "text": "Good place",
      "user_name": "Jane Smith",
      "created_at": "2024-01-14T09:00:00Z"
    }
  ]
}
```

---

## ✨ Key Features & Implementation Details

### 1. Phone-Based Authentication
**Why**: Requirement specified phone number as identifier
**How**: 
- Custom User model with phone as `USERNAME_FIELD`
- Custom authentication backend (`PhoneAuthBackend`)
- Token-based authentication for API

### 2. Smart Place Creation
**Feature**: When adding review, place is auto-created if doesn't exist
**Implementation**: `Place.objects.get_or_create()` in `AddReviewView`
**Benefit**: Users don't need to create places separately

### 3. Intelligent Search Ordering
**Feature**: Exact matches appear before partial matches
**Implementation**: 
```python
.annotate(
    exact_match=Case(
        When(Q(name__iexact=name), then=1),
        default=0,
    )
).order_by("-exact_match", "name")
```
**How it works**: Adds annotation (1 for exact, 0 for partial), sorts by it descending

### 4. Average Rating Calculation
**Feature**: Places show average rating from all reviews
**Implementation**: `Avg("reviews__rating")` annotation in queryset
**Efficiency**: Calculated in database, not in Python

### 5. Custom Review Ordering
**Feature**: User's own reviews appear first in place details
**Implementation**: 
```python
user_reviews = instance.reviews.filter(user=request.user)
other_reviews = instance.reviews.exclude(user=request.user)
ordered_reviews = list(user_reviews) + list(other_reviews)
```

### 6. Unique Constraints
**Feature**: One user per phone, one place per name+address
**Implementation**: 
- User: `unique=True` on phone field
- Place: `UniqueConstraint` on (name, address)
**Benefit**: Prevents duplicate data at database level

---

## 🔐 Authentication Flow

### How Authentication Works

1. **Registration**:
   - User provides name, phone, password
   - Password is hashed (never stored in plain text)
   - User object created in database

2. **Login**:
   - User provides phone and password
   - `PhoneAuthBackend` finds user by phone
   - Password is verified (hashed comparison)
   - Token is created/retrieved and returned

3. **Authenticated Requests**:
   - Client includes token in header: `Authorization: Token <token>`
   - Django REST Framework validates token
   - `request.user` is set to authenticated user
   - View can access `request.user` for user-specific logic

### Security Features
- Passwords are hashed (bcrypt/PBKDF2)
- Tokens are unique and secure
- All endpoints (except register/login) require authentication
- SQL injection prevented by Django ORM
- XSS protection via Django's built-in security

---

## 🚀 How to Run

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step-by-Step Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Installs Django and Django REST Framework

2. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```
   Creates database tables (User, Place, Review)

3. **Populate Sample Data** (Optional):
   ```bash
   python manage.py seed_data
   ```
   Creates 10 users, 5 places, and random reviews

4. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```
   Starts server at `http://localhost:8000`

5. **Test the API**:
   ```bash
   python test_api.py
   ```
   Runs comprehensive tests on all endpoints

### Access Points
- **API Base URL**: `http://localhost:8000`
- **Admin Panel**: `http://localhost:8000/admin/` (requires superuser)
- **API Endpoints**: See README.md for full list

---

## 📝 Interview Talking Points

### Architecture Decisions
1. **Why Django?**: Robust, secure, follows best practices, great ORM
2. **Why Custom User Model?**: Requirement specified phone-based auth
3. **Why Token Auth?**: Stateless, simple, perfect for mobile apps
4. **Why SQLite?**: Easy setup, can switch to PostgreSQL for production

### Code Quality
1. **Separation of Concerns**: Models, Views, Serializers are separate
2. **DRY Principle**: Reusable serializers and views
3. **Database Constraints**: Unique constraints prevent bad data
4. **Validation**: Both model-level and serializer-level validation

### Performance Considerations
1. **Database Annotations**: Average rating calculated in DB, not Python
2. **Efficient Queries**: Uses select_related/prefetch_related where needed
3. **Indexes**: Database indexes on foreign keys (automatic)

### Scalability
1. **Stateless API**: Can scale horizontally
2. **Database Agnostic**: Can switch from SQLite to PostgreSQL easily
3. **Token Auth**: No server-side sessions, easier to scale

---

## 🎓 Key Concepts Explained

### Django ORM
- Object-Relational Mapping: Write Python code instead of SQL
- Example: `User.objects.get(phone="123")` instead of `SELECT * FROM users WHERE phone='123'`

### Serializers
- Convert Python objects ↔ JSON
- Validate incoming data
- Transform data for API responses

### Migrations
- Version control for database schema
- `makemigrations`: Generate migration files
- `migrate`: Apply migrations to database

### Token Authentication
- Stateless: No server-side sessions
- Token stored on client, sent with each request
- Server validates token on each request

---

## 📚 Additional Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **SQLite Documentation**: https://www.sqlite.org/docs.html

---

## ✅ Summary

This project demonstrates:
- ✅ RESTful API design
- ✅ Custom authentication system
- ✅ Complex database queries with aggregations
- ✅ Smart search and filtering
- ✅ Proper Django project structure
- ✅ Production-ready code patterns

**Total Files**: ~15 Python files
**Lines of Code**: ~500-600 lines
**Technologies**: Django, DRF, SQLite, Python
**Time to Build**: Demonstrates full-stack backend development skills

---

*This documentation is comprehensive and interview-ready. Use it to explain the project structure, architecture, and implementation details to interviewers.*

