# Django Scraper Project

This project is a web scraping application built with Django, Celery, and Redis. It allows users to trigger scraping tasks, monitor their status, and fetch scraped data via API endpoints.

---

## **Getting Started**

### **Prerequisites**
- Python 3.x
- Redis
- SQLITE3 (or your configured database)
- Django and required dependencies (install via `requirements.txt`)

---

## **Setup Instructions**

### **1. Install Dependencies**
Install the required Python packages:

```bash
pip install -r requirements.txt
```

### **2. Configure the Database
Run migrations to set up the database schema:

```bash
python manage.py migrate
```

### **3. Start Redis

```bash
redis-server
```

### **4. Start Celery

```bash
celery -A scraper_project worker --loglevel=info
```

### **5. Start the Django Development Server

```bash
python manage.py runserver
```

### **6. Create a superuser to test the scraping (remember username and password)
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