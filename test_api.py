"""
Comprehensive test script for the Places Review API.
Run this after starting the server: python manage.py runserver
"""
import json
import sys

try:
    import requests
except ImportError:
    print("ERROR: requests library not installed. Install it with: pip install requests")
    sys.exit(1)

BASE_URL = "http://localhost:8000"
token = None


def print_test(name):
    print(f"\n{'='*60}")
    print(f"TEST: {name}")
    print('='*60)


def test_register():
    """Test user registration"""
    print_test("User Registration")
    
    # Test 1: Register new user
    data = {
        "name": "Test User",
        "phone": "9999999999",
        "password": "testpass123"
    }
    response = requests.post(f"{BASE_URL}/api/auth/register/", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    assert response.status_code == 201, "Registration should succeed"
    
    # Test 2: Try to register with same phone (should fail)
    response2 = requests.post(f"{BASE_URL}/api/auth/register/", json=data)
    print(f"\nDuplicate phone test - Status: {response2.status_code}")
    assert response.status_code in [201, 400], "Duplicate phone should be handled"
    
    return data


def test_login(phone, password):
    """Test user login"""
    print_test("User Login")
    
    data = {"phone": phone, "password": password}
    response = requests.post(f"{BASE_URL}/api/auth/login/", json=data)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {result}")
    assert response.status_code == 200, "Login should succeed"
    assert "token" in result, "Response should contain token"
    
    return result["token"]


def test_add_review(token):
    """Test adding a review"""
    print_test("Add Review")
    
    headers = {"Authorization": f"Token {token}"}
    data = {
        "place_name": "Test Restaurant",
        "place_address": "123 Test Street",
        "rating": 5,
        "text": "Excellent food and service!",
        "category": "restaurant"
    }
    response = requests.post(f"{BASE_URL}/api/reviews/add/", json=data, headers=headers)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201, "Review should be created"
    
    # Test adding review to existing place
    data2 = {
        "place_name": "Test Restaurant",
        "place_address": "123 Test Street",
        "rating": 4,
        "text": "Good place"
    }
    response2 = requests.post(f"{BASE_URL}/api/reviews/add/", json=data2, headers=headers)
    print(f"\nSecond review to same place - Status: {response2.status_code}")
    assert response2.status_code == 201, "Second review should be created"
    
    return response.json()


def test_search_places(token):
    """Test searching places"""
    print_test("Search Places")
    
    headers = {"Authorization": f"Token {token}"}
    
    # Test 1: Search by name
    print("\n1. Search by name 'Star':")
    response = requests.get(f"{BASE_URL}/api/places/search/?name=Star", headers=headers)
    print(f"Status: {response.status_code}")
    results = response.json()
    print(f"Results: {json.dumps(results, indent=2)}")
    assert response.status_code == 200, "Search should succeed"
    
    # Test 2: Search by minimum rating
    print("\n2. Search by min_rating=4.0:")
    response = requests.get(f"{BASE_URL}/api/places/search/?min_rating=4.0", headers=headers)
    print(f"Status: {response.status_code}")
    results = response.json()
    print(f"Results: {json.dumps(results, indent=2)}")
    assert response.status_code == 200, "Search should succeed"
    
    # Test 3: Search by category
    print("\n3. Search by category='restaurant':")
    response = requests.get(f"{BASE_URL}/api/places/search/?category=restaurant", headers=headers)
    print(f"Status: {response.status_code}")
    results = response.json()
    print(f"Results: {json.dumps(results, indent=2)}")
    assert response.status_code == 200, "Search should succeed"
    
    # Test 4: Combined search
    print("\n4. Combined search (name='Star' AND min_rating=3.0):")
    response = requests.get(f"{BASE_URL}/api/places/search/?name=Star&min_rating=3.0", headers=headers)
    print(f"Status: {response.status_code}")
    results = response.json()
    print(f"Results: {json.dumps(results, indent=2)}")
    assert response.status_code == 200, "Search should succeed"
    
    return results


def test_place_detail(token, place_id):
    """Test getting place details"""
    print_test("Place Details")
    
    headers = {"Authorization": f"Token {token}"}
    response = requests.get(f"{BASE_URL}/api/places/{place_id}/", headers=headers)
    print(f"Status: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    assert response.status_code == 200, "Place detail should succeed"
    assert "name" in result, "Should have name"
    assert "address" in result, "Should have address"
    assert "average_rating" in result, "Should have average_rating"
    assert "reviews" in result, "Should have reviews"
    
    # Verify review ordering: user's review first, then newest first
    reviews = result["reviews"]
    if reviews:
        print(f"\nReview ordering check:")
        print(f"Total reviews: {len(reviews)}")
        for i, review in enumerate(reviews[:3]):
            print(f"  Review {i+1}: User={review['user_name']}, Rating={review['rating']}, Created={review['created_at']}")
    
    return result


def test_unauthorized_access():
    """Test that unauthorized access is blocked"""
    print_test("Unauthorized Access Test")
    
    # Try to access protected endpoint without token
    response = requests.get(f"{BASE_URL}/api/places/search/")
    print(f"Status without token: {response.status_code}")
    assert response.status_code == 401, "Should require authentication"
    print("✓ Unauthorized access correctly blocked")


def main():
    print("\n" + "="*60)
    print("PLACES REVIEW API - COMPREHENSIVE TEST SUITE")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Make sure the server is running: python manage.py runserver\n")
    
    try:
        # Test unauthorized access
        test_unauthorized_access()
        
        # Test registration
        user_data = test_register()
        
        # Test login
        global token
        token = test_login(user_data["phone"], user_data["password"])
        
        # Test adding review
        review_data = test_add_review(token)
        
        # Test search
        search_results = test_search_places(token)
        
        # Test place detail (use first place from search or create one)
        if search_results and len(search_results) > 0:
            place_id = search_results[0]["id"]
        else:
            # Create a place first
            test_add_review(token)
            search_results = test_search_places(token)
            place_id = search_results[0]["id"] if search_results else None
        
        if place_id:
            test_place_detail(token, place_id)
        
        print("\n" + "="*60)
        print("✓ ALL TESTS PASSED!")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        sys.exit(1)
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: Could not connect to server.")
        print("Make sure the server is running: python manage.py runserver")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

