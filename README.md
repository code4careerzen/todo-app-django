
# Todod App

## Django OAuth2 Impl

Sample project to demonstrate Django OAuth2 impl.

## DevOps

pip install django django-ninja pyjwt

django-admin startproject core .

python3 manage.py startapp todos

mkdir -p todos/templates

Open core/settings.py and add 'todos' to INSTALLED_APPS:

todos/models.py

todos/api.py

todos/templates/index.html
todos/templates/list.html

core/urls.py

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver

http://localhost:8000/

pip freeze > requirements.txt