# quick notes

C2
.99 = 458
.9 = 383
.5 = 281
.1 = 183
.01 = 111

C6
.99 = 919
.9 = 802
.5 = 655
.1 = 508
.01 = 393

# startup

WINDOWS
C:\Users\carol\Code\Personal\GenshinWishOracle\venv\Scripts\activate
cd genshinwishoracle
python manage.py runserver

C:\Users\carol\Code\Personal\GenshinWishOracle\venv\Scripts\activate
cd C:\Users\carol\Code\Personal\GenshinWishOracle\genshinwishoracle\recording\
python daily_record.py

MAC
source venv/bin/activate
cd genshinwishoracle
python3 manage.py runserver

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

python manage.py loaddata initial_data_content_types.json
python manage.py loaddata initial_data_users.json
python manage.py loaddata initial_data_auth.json
python manage.py loaddata initial_data_characters_and_weapons.json

# dump data for models

python manage.py dumpdata auth.user users.Profile > users.json
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

- Cyno Weapon
- Baizhu C2
- Some other rando c6
