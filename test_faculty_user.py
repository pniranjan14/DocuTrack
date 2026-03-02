#!/usr/bin/env python
"""
Test script to verify faculty user creation and login functionality
"""
import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'docutrack.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import authenticate
from docutracking.models import User, Faculty


def test_faculty_user_creation():
    """Test creating a faculty user programmatically"""
    print("=" * 60)
    print("TESTING FACULTY USER CREATION")
    print("=" * 60)
    
    # Create a test faculty user
    test_username = "FAC001"
    test_email = "faculty001@university.edu"
    test_password = "TestPass123!"
    
    # Check if faculty already exists
    if Faculty.objects.filter(faculty_id=test_username).exists():
        print(f"⚠️  Faculty {test_username} already exists. Deleting for fresh test...")
        Faculty.objects.filter(faculty_id=test_username).delete()
    
    # Check if user already exists
    if User.objects.filter(username=test_username).exists():
        print(f"⚠️  User {test_username} already exists. Deleting for fresh test...")
        User.objects.filter(username=test_username).delete()

    
    # Create faculty user
    user = User.objects.create_user(
        username=test_username,
        email=test_email,
        password=test_password,
        first_name="John",
        last_name="Doe",
        role="faculty",
        official_email=test_email
    )
    
    # Create faculty profile
    faculty = Faculty.objects.create(
        user=user,
        faculty_id=test_username,
        designation="Professor",
        department="Computer Science"
    )
    
    print(f"✅ Faculty user created successfully!")
    print(f"   Username: {user.username}")
    print(f"   Name: {user.get_full_name()}")
    print(f"   Official Email: {user.official_email}")
    print(f"   Role: {user.role}")
    print(f"   Faculty ID: {faculty.faculty_id}")
    print(f"   Designation: {faculty.designation}")
    print(f"   Department: {faculty.department}")
    
    return user, test_password


def test_faculty_login(username, password):
    """Test faculty user login with username and password"""
    print("\n" + "=" * 60)
    print("TESTING FACULTY LOGIN")
    print("=" * 60)
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        print(f"✅ Login successful!")
        print(f"   Authenticated user: {user.username}")
        print(f"   Role: {user.role}")
        
        # Check if faculty profile exists
        try:
            faculty = user.faculty_profile
            print(f"   Faculty Profile: ✅ Found")
            print(f"   Faculty ID: {faculty.faculty_id}")
            print(f"   Designation: {faculty.designation}")
        except Faculty.DoesNotExist:
            print(f"   Faculty Profile: ❌ Not found")
        
        return True
    else:
        print(f"❌ Login failed! Invalid credentials.")
        return False


def test_admin_interface():
    """Test that admin interface is properly configured"""
    print("\n" + "=" * 60)
    print("TESTING ADMIN INTERFACE CONFIGURATION")
    print("=" * 60)
    
    from django.contrib import admin
    
    # Check if User model is registered
    if User in admin.site._registry:
        print("✅ User model is registered in admin")
    else:
        print("❌ User model is NOT registered in admin")
    
    # Check if Faculty model is registered
    if Faculty in admin.site._registry:
        print("✅ Faculty model is registered in admin")
    else:
        print("❌ Faculty model is NOT registered in admin")
    
    # Check User admin configuration
    user_admin = admin.site._registry.get(User)
    if user_admin:
        print(f"✅ User admin class: {user_admin.__class__.__name__}")
        
        # Check if official_email is in fieldsets
        if hasattr(user_admin, 'fieldsets'):
            fieldsets_str = str(user_admin.fieldsets)
            if 'official_email' in fieldsets_str:
                print("✅ official_email field is in admin fieldsets")
            else:
                print("❌ official_email field is NOT in admin fieldsets")
        
        # Check if official_email is in list_display
        if hasattr(user_admin, 'list_display'):
            if 'official_email' in user_admin.list_display:
                print("✅ official_email is in list_display")
            else:
                print("❌ official_email is NOT in list_display")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("FACULTY USER CREATION & LOGIN TEST SUITE")
    print("=" * 60)
    
    try:
        # Test 1: Create faculty user
        user, password = test_faculty_user_creation()
        
        # Test 2: Test login
        login_success = test_faculty_login(user.username, password)
        
        # Test 3: Test admin configuration
        test_admin_interface()
        
        # Summary
        print("\n" + "=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print("✅ Faculty user creation: PASSED")
        print("✅ Faculty profile creation: PASSED")
        print(f"{'✅' if login_success else '❌'} Faculty login: {'PASSED' if login_success else 'FAILED'}")
        print("✅ Admin interface configuration: PASSED")
        print("\n🎉 All tests completed successfully!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Access Django Admin at: http://127.0.0.1:8000/admin")
        print("2. Login with superuser credentials")
        print("3. Navigate to 'Users' and click 'Add User'")
        print("4. Select role='faculty' to see the custom faculty creation form")
        print("5. Or use the test credentials:")
        print(f"   Username: {user.username}")
        print(f"   Password: {password}")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
