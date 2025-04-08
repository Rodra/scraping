# Django Scraper Project

This project is a web scraping application built with Django, Celery, and Redis. It allows users to trigger scraping tasks, monitor their status, and fetch scraped data via API endpoints. Dec

---

## **Getting Started**

### **Prerequisites**
- Python 3.x
- Redis
- SQLITE3 (or your configured database)
- Django and required dependencies (install via `requirements.txt`)


## **Setup Instructions**

### **1. Create and Activate a Virtual Environment**
Use a virtual environment to isolate dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
```

### **2. Install Dependencies**
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### **3. Configure the Database**
Run migrations to set up the database schema:

```bash
cd src
python manage.py migrate
```

### **4. Start Redis**

```bash
redis-server
```

### **5. Start Celery**

```bash
celery -A scraping_project worker --loglevel=info
```

### **6. Start the Django Development Server**

```bash
python manage.py runserver
```

### **7. Create a superuser to test the scraping (remember username and password)**
```bash
python manage.py createsuperuser
```


## **Usage Workflow**

### **1. Obtain an Authorization Token**
Use the `/api-token-auth/` endpoint to get an authentication token.

#### **Request**
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

#### **Response**
```bash
{
    "refresh": "your_refresh_token",
    "access": "your_generated_token",
}
```


### **2. Trigger a Scrape Task**
Use the `/api/scrape/` endpoint to trigger a scraping task.

#### **Request**
```bash
curl -X POST http://127.0.0.1:8000/api/scrape/ \
     -H "Authorization: Token your_generated_token" \
     -H "Content-Type: application/json" \
     -d '{"username": "your_username", "password": "your_password"}'
```

#### **Response**
```bash
{
    "task_id": "some_task_id"
}
```


### **3. Check Task Status**
Use the `/api/scrape/<task_id>/` endpoint to check the status of a scraping task.

#### **Request**
```bash
curl -X GET http://127.0.0.1:8000/api/scrape/some_task_id/ \
     -H "Authorization: Token your_generated_token"
```

#### **Response**
`Pending Task`
```bash
{
    "status": "PENDING"
}
```

`Successful Task`
```bash
{
    "status": "SUCCESS",
    "result": "Scraped 10 quotes successfully."
}
```

`Failed Task`
```bash
{
    "status": "FAILURE",
    "error": "Some error message"
}
```

### **4. Fetch Scraped Quotes**
Use the `/quotes/` endpoint to fetch all scraped quotes.

#### **Request**
```bash
curl -X GET http://127.0.0.1:8000/api/quotes/ \
     -H "Authorization: Token your_generated_token"
```

#### **Response**
```bash
{
    [
        {
            "id": 1,
            "text": "“The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.”",
            "author": "Albert Einstein",
            "tags": "change, deep-thoughts, thinking, world",
            "goodreads_link": null,
            "created_at": "2025-04-07T14:42:08.041643Z"
        },
        {
            "id": 2,
            "text": "“It is our choices, Harry, that show what we truly are, far more than our abilities.”","author": "J.K. Rowling",
            "tags": "abilities, choices",
            "goodreads_link": null,
            "created_at": "2025-04-07T14:42:08.051452Z"
        }
    ]
}
```

## **What would I do with more time**

With more time and resources, the following improvements could significantly enhance the reliability, scalability, and maintainability of the system:

#### Monitoring & Observability
- Integrate a tool like Datadog or Prometheus to track:
    - Task execution status and failure rates.
    - API response times and queue lengths.
    - Resource usage and performance trends.
- Add structured logging for easier debugging and root cause analysis.

#### Production-Ready Database
- Replace SQLite with PostgreSQL to support:
    - Concurrent access.
    - Better data integrity.
    - Scalability and compatibility with cloud environments.

#### Scalable Task Design
- Refactor Celery usage to:
    - Create separate tasks per portal or scraping strategy.
    - Improve task isolation and parallelism.
    - Allow portal-specific retry and rate-limiting logic.

#### Pluggable Architecture for Scrapers
- Use a Strategy Pattern or similar abstraction to:
    - Support multiple scraping approaches (HTML parsing, APIs, headless browsers, etc.).
    - Onboard new portals with minimal code duplication.
    - Ensure code maintainability and testability.

#### Robust Error Handling
- Improve handling of edge cases like:
    - Structural changes in target websites (e.g., missing HTML elements).
    - Intermittent HTTP errors (e.g., 429 Too Many Requests, 503 Service Unavailable).
- Add fallback behavior or alerting for persistent failures.

#### Authentication & Security
- Prepare for multi-user access with role-based access control (RBAC).
- Secure sensitive configurations using environment variables or a secrets manager.

#### Improved API Response Structure
- Enhance how scraped data is returned from the backend:
    - Format responses into paginated, structured JSON.
    - Allow filtering and sorting via query parameters.
    - Provide meaningful status codes and error messages for frontend or client integration.

### **Dockerization**
- Dockerize the application to simplify deployment and ensure consistency across environments:
    - Create a `Dockerfile` for the Django application.
    - Use `docker-compose` to orchestrate services like Django, Redis, and Celery.
    - Enable easy scaling of workers and services in production environments.

## **Why Django Was Chosen for the MVP**
Django was a practical choice for this MVP due to its built-in support for features that aligned well with the project’s needs:

- Database Modeling: Django’s ORM made it easy to define and manage the data models, which was essential for storing and querying scraped information reliably.

- API Development: Using Django REST Framework allowed for quick setup of clean, structured APIs without a lot of boilerplate, making it easier to expose scrape results and manage job requests.

- Celery Integration: Django works seamlessly with Celery, enabling background task execution with access to the database models and configuration, which was key for handling scraping jobs asynchronously.