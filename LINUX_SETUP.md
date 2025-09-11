# 🐧 Linux Setup Guide for Diary App

This guide helps you set up the diary app on Linux systems.

## Prerequisites

### 1. Install System Dependencies

The app requires system packages for image processing (Pillow). Run these commands based on your Linux distribution:

#### Ubuntu/Debian:
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv python3-dev
sudo apt install libjpeg-dev zlib1g-dev libpng-dev
sudo apt install build-essential
```

#### CentOS/RHEL/Fedora:
```bash
# For CentOS/RHEL
sudo yum install python3 python3-pip python3-devel
sudo yum install libjpeg-devel zlib-devel libpng-devel
sudo yum install gcc gcc-c++ make

# For Fedora
sudo dnf install python3 python3-pip python3-devel
sudo dnf install libjpeg-devel zlib-devel libpng-devel
sudo dnf install gcc gcc-c++ make
```

#### Arch Linux:
```bash
sudo pacman -S python python-pip
sudo pacman -S libjpeg zlib libpng
sudo pacman -S base-devel
```

### 2. Verify Python Installation
```bash
python3 --version  # Should be 3.8 or higher
pip3 --version
```

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/pmnoos/diary_app.git
cd diary_app
```

### 2. Create Virtual Environment
```bash
python3 -m venv diary_env
source diary_env/bin/activate
```

### 3. Upgrade pip (Important!)
```bash
pip install --upgrade pip
```

### 4. Install Requirements
Try one of these approaches:

#### Option A - Install with verbose output (to see what's happening):
```bash
pip install -r requirements.txt -v
```

#### Option B - Install packages individually if you get errors:
```bash
pip install Django>=5.2
pip install Pillow>=10.0.0
pip install sqlparse>=0.5.0
pip install gunicorn>=23.0.0
pip install whitenoise>=6.9.0
pip install dj-database-url>=2.3.0
pip install asgiref>=3.8.1
pip install tzdata>=2025.2
```

#### Option C - Alternative Pillow installation (if Option A fails):
```bash
# Install Django first
pip install Django>=5.2 sqlparse>=0.5.0 asgiref>=3.8.1

# Install Pillow with specific options
pip install --upgrade pip setuptools wheel
pip install Pillow>=10.0.0 --no-cache-dir

# Install remaining packages
pip install gunicorn>=23.0.0 whitenoise>=6.9.0 dj-database-url>=2.3.0 tzdata>=2025.2
```

### 5. Set Up Database
```bash
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the App
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## Common Issues & Solutions

### Issue 1: "error: Microsoft Visual C++ 14.0 is required"
**Solution:** This is a Windows error message that shouldn't appear on Linux. If you see this, you might be in a compatibility layer. Make sure you're using native Linux Python.

### Issue 2: "Failed building wheel for Pillow"
**Solutions:**
1. Install system dependencies (see Prerequisites above)
2. Try: `pip install --upgrade pip setuptools wheel`
3. Try: `pip install Pillow --no-cache-dir`
4. Alternative: `sudo apt install python3-pil` (Ubuntu/Debian)

### Issue 3: "Permission denied" errors
**Solutions:**
1. Make sure you're in the virtual environment: `source diary_env/bin/activate`
2. Don't use `sudo` with pip inside virtual environment
3. Check directory permissions: `ls -la`

### Issue 4: "Command not found: python"
**Solution:** Use `python3` instead of `python` on most Linux systems.

### Issue 5: Virtual environment issues
**Solution:**
```bash
# Remove old environment
rm -rf diary_env

# Create new one
python3 -m venv diary_env
source diary_env/bin/activate
pip install --upgrade pip
```

## Environment Variables (Optional)

Create a `.env` file for production settings:
```bash
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

## Running in Production

### Using Gunicorn:
```bash
# Install gunicorn (already in requirements)
pip install gunicorn

# Collect static files
python manage.py collectstatic

# Run with gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000
```

### Using systemd service (Advanced):
Create `/etc/systemd/system/diary.service`:
```ini
[Unit]
Description=Diary App
After=network.target

[Service]
User=your-username
Group=your-group
WorkingDirectory=/path/to/diary_app
Environment="PATH=/path/to/diary_app/diary_env/bin"
ExecStart=/path/to/diary_app/diary_env/bin/gunicorn --workers 3 --bind unix:/path/to/diary_app/diary.sock core.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
```

## Need Help?

If you're still having issues, run this diagnostic command and share the output:

```bash
# Diagnostic information
echo "=== System Info ==="
uname -a
echo "=== Python Info ==="
python3 --version
pip3 --version
echo "=== Virtual Environment ==="
which python
which pip
echo "=== Package Info ==="
pip list
```

## Alternative: Using Docker (Easy Setup)

If you continue having dependency issues, you can use Docker:

```bash
# Create Dockerfile in project root
cat > Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev libpng-dev \
    && pip install -r requirements.txt
COPY . .
RUN python manage.py migrate
EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
EOF

# Build and run
docker build -t diary-app .
docker run -p 8000:8000 diary-app
```
