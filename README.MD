# EasyLife test task
![Test Status](https://github.com/krch-su/easylife/actions/workflows/ci.yml/badge.svg)
![Coverage Status](./.github/coverage.svg)


## Overview

This project is a test task for a Python developer position, designed to showcase skills in building a robust user management system. The application includes a comprehensive API for managing users and their transactions, a web-based admin panel for data management and statistical insights, and features authentication, role management, and email notifications for specific events.

## Technology Stack

- **Framework:** [Django Ninja](https://django-ninja.rest-framework.com/)
- **Database:** [PostgreSQL](https://www.postgresql.org/)
- **Containerization:** [Docker](https://www.docker.com/)
- **Dependency Management:** [Poetry](https://python-poetry.org/)
- **Testing Framework:** [pytest](https://docs.pytest.org/en/stable/)

## Getting Started

To set up the project, ensure you have Docker and Docker Compose installed on your machine. Follow these steps to build and run the application:

1. **Build and Start the Application:**
    ```bash
    docker-compose build && docker-compose up
    ```
2. **Create Postgres User**

   Inside of docker container execute
   ```bash
    psql -U postgres
    ```
   
   Then
   ```postgres-sql   
    CREATE USER easylife;
    ALTER USER easylife SUPERUSER CREATEDB;
    ALTER USER easylife WITH PASSWORD 'qwertyUIOP';
    CREATE DATABASE easylife;
   ```

3. **Access the Application:**
    ```
    Swagger UI: http://localhost:8010/api/docs
    Admin Panel: http://localhost:8010/admin
    ```
   
4. **Creating a Superuser**

   After the application is running, create a superuser with the following command:

   ```bash
   docker-compose exec manage.py createsuperuser
   ```

5. **Environment Configuration**
Create a .env file in the root directory of the project with the following configuration variables:

   ```dotenv
   JWT_SECRET=hfuh8f0asdyf723h8f22fdskfjlk
   JWT_EXPIRATION_DELTA=0 0:15
   DATABASE_URL=postgres://easylife:qwertyUIOP@db/easylife
   POSTGRES_PASSWORD=qwertyUIOP
   POSTGRES_DB=easylife
   POSTGRES_USER=easylife
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```

## API Access Control
Most API endpoints are restricted to users with the is_staff role. Ensure you provide a valid JWT for a user with the is_staff flag set when accessing these endpoints. You can configure this flag via the admin panel.

## Running Tests
To execute the test suite, run:

```bash
pytest .
```

Before running tests, ensure all development dependencies are installed. You can do this:

**Using requirements-dev.txt**
```bash
pip install -r requirements-test.txt
```


**Or using Poetry**
```bash
poetry install --no-root --with test
```

## Conclusion
This project demonstrates the ability to implement a user management system with essential features and best practices in API development. Contributions and suggestions for improvements are welcome.

