# Sociolite

Backend for a simple social media application, built using django and django-rest-framework.

### Instructions to run locally

_Make sure you have python 3.8 or higher installed and added to system path_

- Clone the repository
- Create a python virtual environment (not necessary, but highly recommended): `$ python -m venv venv`
- Activate the virtual environment: `$ source venv/bin/activate`
- Install dependencies: `$ pip install -r requirements.txt`
- Create a `.env` file with following content:

```
SECRET_KEY=<random-django-secret-key>
DEBUG=True
```

- Apply migrations: `$ python manage.py migrate`
- Start dev server: `$ python manage.py runserver`
