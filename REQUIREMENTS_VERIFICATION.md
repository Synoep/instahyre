# Requirements Verification Report

This document verifies that all requirements from the assignment document are addressed in the project implementation.

## ✅ User Registration

**Requirement:**
- User registers with name and phone number
- Only one user can register with a particular phone number

**Implementation Status:** ✅ **COMPLETE**
- `reviews/models.py`: User model has `name` (line 37) and `phone` (line 38) fields
- `reviews/models.py`: Phone field has `unique=True` constraint (line 38)
- Registration endpoint: `POST /api/auth/register/` (urls.py line 25)

**Note:** Password is also required (assumption documented in README.md line 9-10)

---

## ✅ Authentication

**Requirement:**
- User needs to be logged in to do anything; there is no public access to anything

**Implementation Status:** ✅ **COMPLETE**
- `reviews_api/settings.py`: Default permission class is `IsAuthenticated` (line 99)
- `reviews/views.py`: Register and Login views have `permissions.AllowAny` (lines 20, 24) - correct
- All other endpoints inherit `IsAuthenticated` from settings
- Token authentication configured (settings.py line 96)

---

## ✅ Place Model

**Requirement:**
- Each place has a name and address
- There can only be one place in the database with a particular name and address

**Implementation Status:** ✅ **COMPLETE**
- `reviews/models.py`: Place model has `name` (line 60) and `address` (line 61) fields
- `reviews/models.py`: UniqueConstraint on `name` and `address` (lines 68-71)

**Note:** Category field added (assumption documented in README.md line 11-12)

---

## ✅ Review Model

**Requirement:**
- Review consists of: 1-5 rating, some text, the user who left the review, and when the review was left

**Implementation Status:** ✅ **COMPLETE**
- `reviews/models.py`: Review model has:
  - `rating` with validators MinValueValidator(1), MaxValueValidator(5) (lines 81-83)
  - `text` field (line 84)
  - `user` ForeignKey (line 80)
  - `created_at` DateTimeField with auto_now_add (line 85)

---

## ✅ Add Review Endpoint

**Requirement:**
- User can leave a review by entering place's name, address, and rating
- If place with that name already exists, review is left for it; else a new place is created

**Implementation Status:** ✅ **COMPLETE**
- `reviews/views.py`: AddReviewView uses `get_or_create` (lines 45-51)
- Endpoint: `POST /api/reviews/add/` (urls.py line 28)
- Creates place if it doesn't exist, adds review to existing place if it does

---

## ✅ Search Endpoint

**Requirement:**
- User can search for a place by name and/or minimum rating
- If category is entered, only consider places with that minimum average rating
- If name is entered, any places matching the name fully or partially should be shown
- First places having that exact name should be shown, then places having that name as a substring
- Search results display the name and average rating of each result

**Implementation Status:** ✅ **COMPLETE**
- `reviews/views.py`: SearchPlacesView handles:
  - Name filter with `icontains` (line 88)
  - Min rating filter with `average_rating__gte` (line 79)
  - Category filter (line 84) - implemented as separate filter (assumption)
  - Exact match ordering using `Case/When` with `exact_match` annotation (lines 89-94)
  - Ordering: `-exact_match` (exact matches first), then `name` (line 94)
- `reviews/serializers.py`: PlaceSerializer includes `name` and `average_rating` (line 39)
- Endpoint: `GET /api/places/search/` (urls.py line 30)

**Note:** The requirement text "If a category is entered, then only consider places with that minimum average rating" appears to have a typo. The implementation treats category as a separate filter, which is a reasonable interpretation.

---

## ✅ Search Result Details (Place Details)

**Requirement:**
- Clicking a search result displays all details: name, address, average rating, and all reviews
- For each review, show the name of the user who left it
- If current user has left a review, that review must appear at the top
- All other reviews sorted by newest first

**Implementation Status:** ✅ **COMPLETE**
- `reviews/views.py`: PlaceDetailView (lines 101-117):
  - Retrieves place with average_rating annotation (line 102)
  - Orders reviews: user's reviews first, then others, both by newest first (lines 108-113)
- `reviews/serializers.py`: 
  - PlaceDetailSerializer includes name, address, average_rating, reviews (line 59)
  - ReviewSerializer includes `user_name` field (line 46)
- Endpoint: `GET /api/places/<id>/` (urls.py line 31)

---

## ✅ Data Population

**Requirement:**
- Write a script or other facility that will populate the database with a decent amount of random, sample data

**Implementation Status:** ✅ **COMPLETE**
- `reviews/management/commands/seed_data.py`: Management command that creates:
  - 10 users (lines 17-26)
  - Multiple places with different categories (lines 28-43)
  - Random reviews for places (lines 53-70)
- Can be run with: `python manage.py seed_data` (README.md line 40)

---

## ✅ Instructions on How to Run

**Requirement:**
- Include instructions on how to run your code

**Implementation Status:** ✅ **COMPLETE**
- `README.md`: Comprehensive instructions (lines 17-47):
  - Install dependencies
  - Apply migrations
  - Create superuser (optional)
  - Populate sample data
  - Run development server
- API endpoint documentation included (lines 49-96)

---

## ✅ Additional Requirements

**Requirement:**
- Use Django (preferred)
- Use relational database (strong preference)
- No external services (just web server and database)

**Implementation Status:** ✅ **COMPLETE**
- Django framework used (requirements.txt line 1)
- SQLite (relational database) used (settings.py line 82)
- Token authentication (no external services) (settings.py line 96)
- All assumptions documented in README.md (lines 7-15)

---

## Summary

**All requirements are addressed and implemented correctly.**

The project:
- ✅ Implements all core functionality
- ✅ Uses Django with relational database (SQLite)
- ✅ Has no external service dependencies
- ✅ Includes data population script
- ✅ Has comprehensive README with run instructions
- ✅ Documents all assumptions made
- ✅ Enforces authentication on all protected endpoints
- ✅ Implements correct search ordering logic
- ✅ Implements correct review ordering in place details

**No missing requirements found.**

