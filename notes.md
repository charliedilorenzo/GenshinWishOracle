# quick notes



# startup

WINDOWS
C:\Users\carol\Code\Personal\GenshinWishOracle\venv\Scripts\activate
cd genshinwishoracle
python manage.py runserver

C:\Users\carol\Code\Personal\GenshinWishOracle\venv\Scripts\activate
cd C:\Users\carol\Code\Personal\GenshinWishOracle\genshinwishoracle\recording\
python daily_record.py

MAC
cd GenshinWishOracle
source venv/bin/activate
cd genshinwishoracle
python3 manage.py runserver

cd GenshinWishOracle/genshinwishoracle
/Users/Charlie/Documents/Coding/GenshinWishOracle/GenshinWishOracle/genshinwishoracle
python3 manage.py createsuperuser

IF STATIC CSS ISNT IMPLEMENTED FIRST TRY SHIFT-RELOADING PAGE

# hopefully surefire process if redoing tables manually doesnt work

delete all migrations except folder and init
delete the db
comment out import views and all the urls
python manage.py makemigrations
<!-- python manage.py migrate --fake -->
python manage.py migrate
python manage.py migrate --run-syncdb

# load fixtures

## Current User loading:
// load
python manage.py loaddata test_users.json
// dump
python manage.py dumpdata auth.User users --indent=4 > test_users.json

python manage.py loaddata initial_data_content_types.json; python manage.py loaddata initial_data_characters_and_weapons.json; python manage.py loaddata banners.json;
python manage.py loaddata users.json;
python manage.py loaddata primorecords.json

python manage.py dumpdata auth.User users --indent=4 --natural-foreign > test_users.json

python manage.py loaddata primorecords.json; python manage.py loaddata users.json;


python manage.py loaddata initial_data_content_types.json
python manage.py loaddata initial_data_characters_and_weapons.json
python manage.py loaddata users.json
python manage.py loaddata primorecords.json
python manage.py loaddata banners.json
<!-- python manage.py loaddata users.json -->

python manage.py loaddata initial_data_users.json

# dump data for models

python manage.py dumpdata auth.user users.Profile --indent=4 --natural > users.json
python manage.py dumpdata auth.user --indent=4 --natural-primary > users.json
python manage.py dumpdata users.Profile --indent=4 --natural-foreign > profiles.json
python manage.py dumpdata genshinwishoracle.character > characters.json
python manage.py dumpdata genshinwishoracle.weapon > weapons.json
python manage.py dumpdata genshinwishoracle.banner genshinwishoracle.characterbanner genshinwishoracle.weaponbanner > banners.json
python manage.py dumpdata users.primogemsnapshot users.primogemrecord > primorecords.json

python manage.py dumpdata auth.user users.Profile > initial_data_users.json

# Testing notes

python manage.py test
python manage.py test app.tests.test_name
python manage.py test genshinwishoracle.tests.test_views

coverage run -m pytest
coverage report -m
pytest -k database_test.py

cd C:\Users\carol\Code\Personal\GenshinWishOracle\genshinwishoracle\genshinwishoracle
set  DJANGO_SETTINGS_MODULE=settings

# REQUIREMENTS.TXT NOTES

<<<< pip freeze > requirements.txt >>>>
pip install -r requirements.txt
pip install pipreqs
pipreqs

python -m  pipreqs.pipreqs

# GIT NOTES

git rm --cached .gitignore

# VirtualEnv NOTES

C:\Users\carol\AppData\Local\Programs\Python\Python39\python.exe
virtualenv --python C:\Users\carol\AppData\Local\Programs\Python\Python39\python.exe venv
<!-- virtualenv --python  venv -->

WINDOWS
.\venv\Scripts\activate

MAC
source venv/bin/activate

deactivate

pip freeze > requirements.txt

pip install -r requirements.txt

# WEAPONS AVAILABILITY

<https://genshin-impact.fandom.com/wiki/Weapon/List/By_Availability>

# New Plan

- Baizhu C2
- Kazuha
- Cyno Weapon
- Some other rando c6


# For if we want to switch to a custom user

from django.contrib.auth import get_user_model

relevant files: (with searching from users.models import Profile)
/genshinwishoracle/analyze/views.py
/genshinwishoracle/genshinwishoracle/forms.py
/genshinwishoracle/genshinwishoracle/helpers.py
/genshinwishoracle/genshinwishoracle/views.py
/genshinwishoracle/genshinwishoracle/tests/test_forms.py
/genshinwishoracle/genshinwishoracle/tests/test_helpers.py
/genshinwishoracle/genshinwishoracle/tests/test_models.py
/genshinwishoracle/genshinwishoracle/tests/test_views.py
/genshinwishoracle/users/forms.py
/genshinwishoracle/users/tests/test_models.py
/genshinwishoracle/users/tests/test_views.py
