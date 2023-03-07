# startup

.\venv\Scripts\activate
cd genshinwishoracle
python manage.py runserver

IF STATIC CSS ISNT IMPLEMENTED FIRST TRY SHIFT-RELOADING PAGE

DROP TABLE analyze_banner;
DROP TABLE analyze_weaponbanner;
DROP TABLE analyze_characterbanner;
DROP TABLE analyze_weaponbanner_rateups;
DROP TABLE analyze_characterbanner_rateups;
DROP TABLE users_profile_banners;
DROP TABLE users_profile_characterbanners;
DROP TABLE users_profile_weaponbanners;

DROP TABLE analyze_banner;
DROP TABLE analyze_weaponbanner;
DROP TABLE analyze_characterbanner;
DROP TABLE analyze_weaponbanner_rateups;
DROP TABLE analyze_characterbanner_rateups;
DROP TABLE users_profile_banners;

CREATE TABLE IF NOT EXISTS analyze_characterbanner(
    banner_ptr_id INT
);

CREATE TABLE IF NOT EXISTS analyze_weaponbanner (
    banner_ptr_id INT
);

CREATE TABLE IF NOT EXISTS analyze_banner (
    id INT PRIMARY KEY,
    name TEXT,
    enddate DATE,
    banner_type TEXT
);
CREATE TABLE IF NOT EXISTS analyze_weaponbanner_rateups(
    id INT PRIMARY KEY,
    weaponbanner INT,
    weapon_id INT
);
CREATE TABLE IF NOT EXISTS analyze_characterbanner_rateups(
    id INT PRIMARY KEY,
    characterbanner INT,
    character_id INT
);

CREATE TABLE IF NOT EXISTS users_profile_banners(
    id INT PRIMARY KEY,
    profile_id INT,
    banner_id INT
);

# hopefully surefire process if redoing tables manually doesnt work

delete all migrations except folder and init
delete the db
comment out import views and all the urls
python manage.py makemigrations
<!-- python manage.py migrate --fake -->
python manage.py migrate
python manage.py migrate --run-syncdb
python manage.py loaddata initial_data_content_types.json
python manage.py loaddata initial_data_users.json
python manage.py loaddata initial_data_auth.json
python manage.py loaddata initial_data_character_and_weapons.json

python manage.py dumpdata auth users.Profile > users.json
python manage.py dumpdata analyze.character > characters.json
python manage.py dumpdata analyze.weapon > weapons.json
python manage.py dumpdata analyze.banner analyze.characterbanner analyze.weaponbanner > banners.json

python manage.py loaddata initial_data_content_types.json
python manage.py loaddata initial_data_users.json
python manage.py loaddata initial_data_auth.json
python manage.py loaddata initial_data_character_and_weapons.json

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
