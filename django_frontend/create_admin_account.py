#!/usr/bin/env python
"""
Script to create an admin account for accessing the admin section.
Usage: python create_admin_account.py
"""

import os
import sys
import django
import requests

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin_account():
    """Create Django user and register in FastAPI admin_users."""
    
    print("=" * 60)
    print("Admin Account Creation")
    print("=" * 60)
    
    username = input("\nEnter username (default: admin): ").strip() or "admin"
    email = input("Enter email (default: admin@staycation.com): ").strip() or "admin@staycation.com"
    password = input("Enter password: ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"❌ User '{username}' already exists!")
        return
    
    try:
        # Create Django user
        print(f"\n📝 Creating Django user '{username}'...")
        User.objects.create_user(username=username, password=password, email=email)
        print(f"✅ Django user '{username}' created successfully!")
        
        # Create FastAPI admin user
        print(f"\n📝 Creating FastAPI admin user...")
        api_base = os.environ.get('FASTAPI_URL', 'http://127.0.0.1:8001')
        
        user_data = {
            "username": username,
            "email": email,
            "full_name": username.capitalize(),
            "password": password
        }
        
        resp = requests.post(f"{api_base}/api/users", json=user_data, timeout=5)
        
        if resp.status_code in [200, 201]:
            print(f"✅ FastAPI admin user created successfully!")
            print(f"\n{'=' * 60}")
            print("✅ Admin Account Created Successfully!")
            print(f"{'=' * 60}")
            print(f"\n📧 Username: {username}")
            print(f"🔐 Password: {'*' * len(password)}")
            print(f"📬 Email: {email}")
            print(f"\nYou can now login at: http://localhost:8000/login/")
            print(f"{'=' * 60}\n")
        else:
            print(f"⚠️  FastAPI user creation response: {resp.status_code}")
            print(f"Response: {resp.text}")
            print(f"\n⚠️  Django user was created, but FastAPI user creation may have failed.")
            print(f"You may need to manually add this user to the admin list.")
            
    except requests.exceptions.ConnectionError:
        print(f"\n❌ Cannot connect to FastAPI at {api_base}")
        print(f"Make sure FastAPI is running on port 8001")
        print(f"\nDjango user was created, but FastAPI user was not.")
        return
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return

if __name__ == '__main__':
    create_admin_account()
