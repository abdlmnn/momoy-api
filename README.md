# 🐾 Momoy Pet Supplies – DJANGO REST Framework

This repository contains the python DJANGO REST API for **Momoy Pet Supplies**.

---

## Download

1. DOWNLOAD PYTHON, IF YOU HAVEN'T DOWNLOAD:

- OPEN LINK **https://www.python.org/downloads/**

2. DOWNLOAD PIP, IF YOU HAVEN'T DOWNLOAD:

- OPEN LINK **https://bootstrap.pypa.io/get-pip.py**
  CTRL S
  Save files inside of your folder

---

## Prerequisites

Before running the commands, make sure you have:

- **Python** → version 3.13.7 or later

```bash
  python --version
```

OR

```bash
  py --version
```

- Install and check version of **pip**

```bash
  python get-pip.py
```

```bash
  pip --version
```

---

## Virtual Environment

- Install virtual environtment

```bash
  pip install pipenv
```

- Set up virtual environtment

```bash
  pipenv shell
```

---

## Requirements

- Crate a file **requirements.txt** and copy and paste it

```php
django
djangorestframework
django-allauth
environs
pillow
python-dotenv
requests
cryptography
social-auth-app-django
pipenv
django-cors-headers
python-decouple
psycopg2-binary
```

- Install the file **requirements.txt**

```bash
  pip install -r requirements.txt
```

- Optional if you want to verify installation

```bash
  pip list
```

---

## Project & App

1. Create a project

```bash
  django-admin startproject name_project
```

- Optional if you want your project folder will be as the root

```bash
  django-admin startproject name_project .
```

- Folder structure

```bash
  rootFolder/
  ├── name_project/ # This is your project
  │   ├── _init_.py
  │   ├── asgi.py
  │   ├── settings.py
  │   ├── urls.py
  │   ├── wsgi.py
  ├── manage.py
  ├── Pipfile
  ├── README.md
  └── requirements.txt
```

2. Create a app

```bash
  py manage.py startapp name_app
```

- Folder structure

```bash
  rootFolder/
  ├── name_app/ # This is your app
  ├── name_project/
  │   ├── _init_.py
  │   ├── asgi.py
  │   ├── settings.py
  │   ├── urls.py
  │   ├── wsgi.py
  ├── manage.py
  ├── Pipfile
  ├── README.md
  └── requirements.txt
```

3. Config your Settings.py

- Open name_project -> settings.py

Take Note: Everytime you create App always add your app in settings.py

```py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Add REST Framework, CORS, Social login
    "rest_framework",
    "corsheaders",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "social_django",

    # Here add you app
    "name_app",

]
```

```py
  MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    "corsheaders.middleware.CorsMiddleware", # Add this and must be above CommonMiddleware

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    "allauth.account.middleware.AccountMiddleware", # Add the allauth here

    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
  ]

  CORS_ALLOW_ALL_ORIGINS = True # Add this for CORS (Expo communiting for DJANGO)
```

Copy and Paste this for REST_FRAMEWORK

```py
  REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        # later: add JWT authentication here
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
  }
```
