#!/usr/bin/env python3
"""
Quick setup script for the Django Diary PWA
Run this after cloning the repository
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error: {e.stderr}")
        return False

def main():
    print("🚀 Setting up Django Diary PWA...")
    print("=" * 50)
    
    # Check if we're in a virtual environment
    if sys.prefix == sys.base_prefix:
        print("⚠️  Warning: You're not in a virtual environment!")
        print("   Recommended: Create and activate a virtual environment first")
        print("   python -m venv diary && diary\\Scripts\\activate  # Windows")
        print("   python -m venv diary && source diary/bin/activate  # macOS/Linux")
        choice = input("   Continue anyway? (y/N): ")
        if choice.lower() != 'y':
            sys.exit(0)
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py makemigrations", "Creating migrations"):
        sys.exit(1)
    
    if not run_command("python manage.py migrate", "Applying migrations"):
        sys.exit(1)
    
    # Ask about demo data
    print("\n📝 Demo data setup:")
    choice = input("   Create demo entries to showcase the app? (Y/n): ")
    if choice.lower() != 'n':
        if run_command("python manage.py shell -c \"from entries.demo_data import create_demo_data; create_demo_data()\"", "Creating demo data"):
            print("   Demo user: demo_user (password: demo123)")
    
    # Success message
    print("\n" + "=" * 50)
    print("🎉 Setup complete!")
    print("\nNext steps:")
    print("1. Run the server: python manage.py runserver")
    print("2. Open your browser: http://127.0.0.1:8000")
    print("3. Create an account or use demo_user/demo123")
    print("4. Try the PWA features (install, offline mode)")
    print("\n📖 Check README.md for more information")

if __name__ == "__main__":
    main()
