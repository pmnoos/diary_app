# My Personal Diary App

A Progressive Web App (PWA) built with Django that allows users to write, manage, and organize their personal diary entries with offline functionality.

## Features

- 📝 **Rich Text Entries** - Write diary entries with text, images, and links
- 🔐 **User Authentication** - Secure login/signup system
- 📱 **Progressive Web App** - Works offline and can be installed like a native app
- 🌙 **Privacy Controls** - Mark entries as private or public
- 🎨 **Demo Mode** - Showcase app capabilities with sample entries
- 💾 **Offline Support** - Write entries offline, auto-sync when online
- 📷 **Image Uploads** - Add photos to your diary entries
- 🔗 **Smart Links** - Automatically convert URLs to clickable links

## Tech Stack

- **Backend**: Django 5.2 with Python 3.13
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **PWA**: Service Workers, Web App Manifest, IndexedDB
- **Deployment**: Ready for Heroku, Railway, or any WSGI host

## Quick Start

### Prerequisites

- Python 3.13+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/pmnoos/diary_app.git
   cd diary_app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv diary
   
   # Windows
   diary\Scripts\activate
   
   # macOS/Linux
   source diary/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create demo data (optional)**
   ```bash
   python manage.py shell
   >>> from entries.demo_data import create_demo_data
   >>> create_demo_data()
   >>> exit()
   ```

6. **Run the server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser** to `http://127.0.0.1:8000`

## Usage

### Creating Your First Entry

1. Sign up for a new account or login
2. Click "New Entry" in the navigation
3. Write your diary entry with optional images and links
4. Choose privacy setting (private/public)
5. Save your entry

### PWA Features

- **Install the app**: Look for the install button in your browser
- **Offline writing**: Works without internet connection
- **Auto-sync**: Offline entries sync when you're back online

### Demo Mode

Visit the homepage to see the app in action with sample entries that showcase all features.

## Development

### Project Structure

```
diary_app/
├── core/                 # Django project settings
├── accounts/             # User authentication
├── entries/              # Main diary functionality
│   ├── static/          # CSS, JS, icons, service worker
│   ├── templates/       # HTML templates
│   └── migrations/      # Database migrations
├── requirements.txt     # Development dependencies
├── requirements-production.txt  # Production dependencies
└── manage.py           # Django management script
```

### Key Features Implementation

- **PWA**: Service worker caching and offline functionality
- **Authentication**: Django's built-in auth with custom templates
- **Image handling**: Pillow for image processing and uploads
- **Link conversion**: Custom template filter for URL detection
- **Responsive design**: Mobile-first CSS with clean styling

## Deployment

The app is ready for production deployment:

### Heroku

```bash
# Install Heroku CLI and login
heroku create your-diary-app
git push heroku main
heroku run python manage.py migrate
```

### Railway

```bash
# Install Railway CLI and login
railway new
railway add
railway deploy
```

### Environment Variables

For production, set these environment variables:

- `DEBUG=False`
- `SECRET_KEY=your-secret-key`
- `DATABASE_URL=your-database-url` (for PostgreSQL)
- `ALLOWED_HOSTS=your-domain.com`

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Django framework
- PWA implementation inspired by web standards
- Icons created using SVG for scalability
- Demo data showcases real-world usage

## Screenshots

| Desktop View | Mobile View | PWA Install |
|--------------|-------------|-------------|
| ![Desktop](screenshots/desktop.png) | ![Mobile](screenshots/mobile.png) | ![Install](screenshots/install.png) |

---

**Start capturing your thoughts today!** 📔✨
