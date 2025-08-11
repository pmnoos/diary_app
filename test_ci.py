#!/usr/bin/env python3
"""
Test runner script for the Django Diary app
Mimics the CI environment locally
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
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        if e.stdout:
            print(f"   Output: {e.stdout}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False

def main():
    print("🧪 Running CI/CD Tests Locally...")
    print("=" * 50)
    
    # Set environment variable
    os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings_test'
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        sys.exit(1)
    
    # Run migrations
    if not run_command("python manage.py migrate", "Running migrations"):
        sys.exit(1)
    
    # Run tests
    if not run_command("python manage.py test --verbosity=2", "Running tests"):
        sys.exit(1)
    
    # Success message
    print("\n" + "=" * 50)
    print("✅ All tests passed! Your code is ready for GitHub.")
    print("\nThis matches what GitHub Actions will run.")

if __name__ == "__main__":
    main()
