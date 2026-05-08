#!/usr/bin/env python
"""
Test script for Pet Adoption API Authentication

This script demonstrates:
1. User registration
2. User login
3. Using JWT token for authenticated requests
4. CRUD operations on pets
"""

import requests
import json

# Configuration
BASE_URL = "http://127.0.0.1:8000/api"

def test_registration():
    """Test user registration."""
    print("🔐 Testing User Registration...")

    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "password_confirm": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/auth/register/", json=data)

    if response.status_code == 201:
        result = response.json()
        print("✅ Registration successful!")
        print(f"User: {result['user']['username']}")
        print(f"Access Token: {result['tokens']['access'][:50]}...")
        return result['tokens']
    else:
        print(f"❌ Registration failed: {response.json()}")
        return None

def test_login():
    """Test user login."""
    print("\n🔑 Testing User Login...")

    data = {
        "username": "testuser",
        "password": "testpassword123"
    }

    response = requests.post(f"{BASE_URL}/auth/login/", json=data)

    if response.status_code == 200:
        result = response.json()
        print("✅ Login successful!")
        print(f"Access Token: {result['tokens']['access'][:50]}...")
        return result['tokens']
    else:
        print(f"❌ Login failed: {response.json()}")
        return None

def test_get_pets(token):
    """Test getting all pets."""
    print("\n🐾 Testing Get All Pets...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{BASE_URL}/pets/", headers=headers)

    if response.status_code == 200:
        result = response.json()
        print(f"✅ Found {result['count']} pets!")
        return result['results']
    else:
        print(f"❌ Failed to get pets: {response.json()}")
        return []

def test_create_pet(token):
    """Test creating a new pet."""
    print("\n➕ Testing Create Pet...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "name": "Test Pet",
        "species": "Dog",
        "breed": "Test Breed",
        "age": 2,
        "description": "A test pet created via API",
        "status": "available",
        "image": "https://example.com/test-pet.jpg"
    }

    response = requests.post(f"{BASE_URL}/pets/create/", json=data, headers=headers)

    if response.status_code == 201:
        result = response.json()
        print("✅ Pet created successfully!")
        print(f"Pet: {result['pet']['name']} (ID: {result['pet']['id']})")
        return result['pet']['id']
    else:
        print(f"❌ Failed to create pet: {response.json()}")
        return None

def test_update_pet(token, pet_id):
    """Test updating a pet."""
    print(f"\n✏️  Testing Update Pet (ID: {pet_id})...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    data = {
        "name": "Updated Test Pet",
        "description": "Updated description via API"
    }

    response = requests.put(f"{BASE_URL}/pets/{pet_id}/update/", json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        print("✅ Pet updated successfully!")
        print(f"Updated name: {result['pet']['name']}")
    else:
        print(f"❌ Failed to update pet: {response.json()}")

def test_get_user_profile(token):
    """Test getting user profile."""
    print("\n👤 Testing Get User Profile...")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    response = requests.get(f"{BASE_URL}/auth/profile/", headers=headers)

    if response.status_code == 200:
        result = response.json()
        print("✅ Profile retrieved successfully!")
        print(f"Username: {result['username']}")
        print(f"Email: {result['email']}")
    else:
        print(f"❌ Failed to get profile: {response.json()}")

def main():
    """Run all authentication tests."""
    print("🚀 Starting Pet Adoption API Authentication Tests")
    print("=" * 50)

    # Test registration
    tokens = test_registration()
    if not tokens:
        # If registration fails, try login (user might already exist)
        tokens = test_login()

    if not tokens:
        print("❌ Cannot proceed without authentication tokens")
        return

    access_token = tokens['access']

    # Test authenticated endpoints
    test_get_user_profile(access_token)
    pets = test_get_pets(access_token)
    pet_id = test_create_pet(access_token)

    if pet_id:
        test_update_pet(access_token, pet_id)

    print("\n" + "=" * 50)
    print("🎉 Authentication tests completed!")
    print("\n💡 To use these tokens in your application:")
    print(f"Authorization: Bearer {access_token}")

if __name__ == "__main__":
    main()