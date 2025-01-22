# Tasks Management System

## Project start.

````
git clone https://github.com/franzferdinnand/Task_management_system.git
pip install -r requirements.txt
````
Then apply migrations:
```
python src/manage.py makemigrations
python src/manage.py migrate
```

Make sure that .env file is in the root directory (with requirements.txt file)

To create a superuser:

```
python src/manage.py createsuperuser
```
### To run the project you need to start 4 services (in terminal) in order:

#### 1. Redis
```
redis-server
```
#### 2. Django server
```
python src/manage.py runserver 8182
```
#### 3. Celery
```
cd src/
celery -A config worker --loglevel=info
```
#### 4. WebSocket server (Daphne)
```
cd src/
daphne -p 8282 config.asgi:application
```

# USERS
#### Methods:
- ![текст](https://img.shields.io/badge/GET-%2390EE90)
- ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)
- ![текст](https://img.shields.io/badge/POST-%23FFFF00)
- ![текст](https://img.shields.io/badge/PUT-%230000FF)
- ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
- ![текст](https://img.shields.io/badge/DELETE-%23FF0000)

### LOGIN

After creating user or superuser you can login in application.

Send POST request with username and password on URL:

#### **LOGIN**: http://localhost:8181/api/v1/auth/login/

### LOGOUT

Logging out is sending refresh token to a blacklist, so user can have an access to application until access token is expired

Send POST request with username and password on URL:

#### **LOGOUT**: http://localhost:8181/api/v1/auth/logout/


# TASKS

#### ➡️ **URL**: [http://localhost:8181/api/v1/tasks/](http://localhost:8181/api/v1/administrators/)

### Methods


- ![текст](https://img.shields.io/badge/GET-%2390EE90)
- ![текст](https://img.shields.io/badge/GET/{id}-%2390EE90)
- ![текст](https://img.shields.io/badge/POST-%23FFFF00)
- ![текст](https://img.shields.io/badge/PUT-%230000FF)
- ![текст](https://img.shields.io/badge/PATCH-%23DDA0DD)
- ![текст](https://img.shields.io/badge/DELETE-%23FF0000)

### Filters
You can filter tasks by status, priority and created_at fields

example 

#### **URL**: http://localhost:8181/api/v1/tasks/?status=2

### Pagination

Default page size is set on 10 results, but you can set another in request with "pageSize":

#### **URL**: http://localhost:8181/api/v1/tasks/?pageSize=5


    
    
