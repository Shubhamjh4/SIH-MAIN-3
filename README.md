# Rural Learning Platform

A comprehensive gamified learning platform designed specifically for rural education, featuring offline-first capabilities, multilingual support, and advanced content synchronization.

## 🌟 Features

### Core Features
- **User Authentication & Management**: Secure user registration, login, and email verification
- **Course Management**: Complete course creation, lesson management, and content organization
- **Gamification System**: Points, badges, achievements, and leaderboards to motivate learners
- **Offline-First Architecture**: Content synchronization for areas with limited internet connectivity
- **Multilingual Support**: English, Hindi (हिन्दी), and Odia (ଓଡ଼ିଆ) language support
- **Progress Tracking**: Detailed analytics and progress monitoring for students and educators
- **Interactive Games**: Educational games for subjects like Mathematics, Physics, Chemistry, and Logic

### Technical Features
- **RESTful API**: Complete API with Swagger documentation
- **JWT Authentication**: Secure token-based authentication
- **Background Tasks**: Celery integration for async processing
- **Caching**: Redis-based caching for improved performance
- **Content Versioning**: Advanced sync system for offline content management
- **Responsive Design**: Mobile-friendly interface for various devices

## 🚀 Quick Start

### Prerequisites
- **Python 3.8+** (Recommended: Python 3.11+)
- **Redis Server** (for caching and background tasks)
- **PostgreSQL** (for production deployment)
- **Git** (for version control)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd SIH_PROJECT
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python3 -m venv .venv
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Copy the example environment file
cp env.example .env

# Edit .env with your configuration
# See Environment Variables section below
```

5. **Run database migrations**
```bash
python manage.py migrate
```

6. **Create a superuser account**
```bash
python manage.py createsuperuser
```

7. **Load sample data (optional)**
```bash
python manage.py create_sample_courses
```

8. **Start the development server**
```bash
# Windows - Start all services (Redis, Celery, Django)
start_services.bat

# Manual start (Linux/Mac)
redis-server &
celery -A learning_platform worker --loglevel=info &
python manage.py runserver
```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 🏗️ Project Structure

```
SIH_PROJECT/
├── accounts/                 # User management and authentication
├── courses/                  # Educational content management
├── gamification/            # Points, badges, and achievements
├── sync/                    # Offline synchronization system
├── learning_platform/       # Main Django project settings
├── templates/               # HTML templates
├── static/                  # Static files (CSS, JS, images, games)
├── media/                   # User uploaded files
├── locale/                  # Internationalization files
└── requirements.txt         # Python dependencies
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Production)
DATABASE_URL=postgresql://user:password@localhost:5432/learning_platform

# Redis Configuration
REDIS_HOST=127.0.0.1
REDIS_PORT=6379
REDIS_PASSWORD=

# Email Configuration (Production)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=your-email@gmail.com

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

### Settings Files

The project uses different settings for different environments:

- `learning_platform/settings.py` - Base settings
- `learning_platform/settings_dev.py` - Development settings
- `learning_platform/settings_prod.py` - Production settings

## 🎮 Apps Overview

### Accounts App
- User registration and authentication
- Email verification system
- Password reset functionality
- User profile management

### Courses App
- Course creation and management
- Lesson organization
- Content file handling
- Progress tracking
- Quiz system
- Subject categorization

### Gamification App
- Point system for user engagement
- Badge and achievement system
- Leaderboard functionality
- Progress rewards

### Sync App
- Offline content synchronization
- Content versioning
- Background sync tasks
- Conflict resolution

## 🌐 API Endpoints

### Authentication
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login
- `POST /api/accounts/logout/` - User logout
- `POST /api/accounts/verify-email/` - Email verification

### Courses
- `GET /api/courses/` - List all courses
- `POST /api/courses/` - Create new course
- `GET /api/courses/{id}/` - Course details
- `PUT /api/courses/{id}/` - Update course
- `DELETE /api/courses/{id}/` - Delete course

### Gamification
- `GET /api/gamification/leaderboard/` - Get leaderboard
- `GET /api/gamification/achievements/` - User achievements
- `POST /api/gamification/points/` - Award points

### Sync
- `GET /api/sync/check/` - Check for updates
- `POST /api/sync/download/` - Download content
- `POST /api/sync/upload/` - Upload progress

## 🎯 Educational Games

The platform includes interactive games for various subjects:

- **Mathematics**: Number games, algebra puzzles, geometry challenges
- **Physics**: Motion simulations, force calculations, energy concepts
- **Chemistry**: Element matching, compound building, reaction simulations
- **Logic**: Puzzle solving, pattern recognition, critical thinking

Access games at: http://localhost:8000/games/

## 🌍 Internationalization

The platform supports multiple languages:

- **English** (en) - Default language
- **Hindi** (hi) - हिन्दी
- **Odia** (or) - ଓଡ଼ିଆ

Language files are located in the `locale/` directory. To add new languages or update translations, use Django's internationalization framework.

## 🚀 Deployment

### Production Deployment

1. **Set up production environment**
```bash
# Use production settings
export DJANGO_SETTINGS_MODULE=learning_platform.settings_prod

# Install production dependencies
pip install gunicorn whitenoise psycopg2-binary
```

2. **Configure production database**
```bash
# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
```

3. **Start production server**
```bash
gunicorn learning_platform.wsgi:application --bind 0.0.0.0:8000
```

### Docker Deployment (Optional)

```dockerfile
# Example Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "learning_platform.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the API documentation at `/swagger/`

## 🔄 Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added gamification system
- **v1.2.0** - Implemented offline sync capabilities
- **v1.3.0** - Added multilingual support

---

**Built with ❤️ for rural education**
