startup:
.\venv\Scripts\activate
cd genshinwishoracle
python manage.py runserver

IF STATIC CSS ISNT IMPLEMENTED FIRST TRY SHIFT-RELOADING PAGE

1. Remove all the migration files

get rid of all */migrations/*.py" -not -name "__init__.py" -delete
get rid of all "*/migrations/*.pyc"
2. Delete db.sqlite3

rm db.sqlite3
3. Create and run the migrations:

python manage.py makemigrations
python manage.py migrate
4. Sync the database:
python manage.py migrate --run-syncdb

# for a specific table

<!-- from django.contrib.auth.models import User -->
python manage.py dumpdata auth users.Profile > users.json
python manage.py dumpdata analyze.character > characters.json
python manage.py dumpdata analyze.weapon > weapons.json
python manage.py dumpdata analyze.banner analyze.characterbanner analyze.weaponbanner > banners.json
python manage.py loaddata initial_data.json

python manage.py makemigrations
python manage.py sqlmigrate
python manage.py migrate
python manage.py runserver

python manage.py shell

python manage.py test analyze

# PYTEST NOTES

coverage run -m pytest
coverage report -m
pytest -k database_test.py

# REQUIREMENTS.TXT NOTES

<<<< pip freeze > requirements.txt >>>>

pip install pipreqs
pipreqs

python -m  pipreqs.pipreqs

# GIT NOTES

git rm --cached .gitignore

# VirtualEnv NOTES

C:\Users\carol\AppData\Local\Programs\Python\Python39\python.exe
virtualenv --python C:\Users\carol\AppData\Local\Programs\Python\Python39\python.exe venv
<!-- virtualenv --python  venv -->

.\venv\Scripts\activate

deactivate

pip freeze > requirements.txt

pip install -r requirements.txt

# WEAPONS AVAILABILITY

<https://genshin-impact.fandom.com/wiki/Weapon/List/By_Availability>
