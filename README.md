![Image](https://github.com/user-attachments/assets/fefd6798-9689-4675-95a0-79791da20adf)

# Django REST API Project

A robust Django REST API project with built-in JWT authentication, Swagger documentation, AWS S3 storage integration, and debugging tools. This project provides a solid foundation for building scalable and well-documented web APIs.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.12 or higher
- pipenv (for dependency management)
- Git

## Installation

Follow these steps to set up the project locally:

1. Clone the repository:
   ```
   git clone https://github.com/Bloul-Mohamed/django_core_project.git 
   cd django-core   ```

2. Install dependencies using pipenv:
   ```
   pipenv install
   ```

3. Activate the virtual environment:
   ```
   pipenv shell
   ```

4. Set up environment variables (create a `.env` file in the project root):
   ```
   DEBUG=True
   SECRET_KEY=your_secret_key
   DATABASE_URL=your_database_url
   AWS_ACCESS_KEY_ID=your_aws_access_key
   AWS_SECRET_ACCESS_KEY=your_aws_secret_key
   AWS_STORAGE_BUCKET_NAME=your_s3_bucket_name
   ```

5. Run database migrations:
   ```
   python manage.py migrate
   ```

## Running the Project

To run the development server:

```
python manage.py runserver
```

The API will be available at http://127.0.0.1:8000/

- API documentation (Swagger UI): http://127.0.0.1:8000/
- Admin interface: http://127.0.0.1:8000/admin/

## Key Dependencies

The project relies on several powerful packages:

- **Django**: High-level Python web framework
- **Django REST Framework**: Toolkit for building Web APIs
- **djangorestframework-simplejwt**: JWT authentication for Django REST Framework
- **drf-yasg**: Swagger/OpenAPI documentation generator
- **django-storages & boto3**: AWS S3 integration for file storage
- **django-debug-toolbar**: Debug panel for development
- **django-environ**: Environment variable handling

## Development

To create a superuser for admin access:

```
python manage.py createsuperuser
```

To run tests:

```
python manage.py test
```

## Deployment

For production deployment:

1. Set `DEBUG=False` in your environment variables
2. Configure your production database
3. Set up proper security measures (HTTPS, secure cookies, etc.)
4. Configure your web server (Gunicorn, Nginx, etc.)

