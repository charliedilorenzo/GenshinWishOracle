# startup

WINDOWS
.\venv\Scripts\activate
cd genshinwishoracle
python manage.py runserver

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

python manage.py dumpdata auth.user users.Profile > initial_data_users.json

# Testing notes

python manage.py test
python manage.py test app.tests.test_name

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

WINDOWS
.\venv\Scripts\activate

MAC
source venv/bin/activate

deactivate

pip freeze > requirements.txt

pip install -r requirements.txt

# WEAPONS AVAILABILITY

<https://genshin-impact.fandom.com/wiki/Weapon/List/By_Availability>

# Manually make tables

python manage.py dbshell

DROP TABLE analyze_character;
DROP TABLE analyze_weapon;
DROP TABLE analyze_banner;
DROP TABLE analyze_weaponbanner;
DROP TABLE analyze_characterbanner;
DROP TABLE analyze_weaponbanner_rateups;
DROP TABLE analyze_characterbanner_rateups;
DROP TABLE users_profile_banners;
DROP TABLE users_profile;
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

DROP TABLE users_profile_banners;
DROP TABLE users_profile;

CREATE TABLE IF NOT EXISTS users_profile(
    id INT PRIMARY KEY,
    numprimos INT,
    numgenesis INT,
    numstarglitter INT,
    numfates INT,
    character_pity INT,
    character_guaranteed BOOL,
    weapon_pity INT,
    weapon_guaranteed INT,
    weapon_fate_points INT,
    welkin_user BOOL,
    battlepass_user BOOL,
    user_id INT
);

CREATE TABLE IF NOT EXISTS users_profile_banners(
    id INT PRIMARY KEY,
    profile_id INT,
    banner_id INT
);

INSERT INTO users_profile (id, numprimos,numgenesis, numgenesis, numfates, numstarglitter, character_pity, character_guaranteed, weapon_pity, weapon_guaranteed, weapon_fate_points, welkin_user, battlepass_user, user_id) VALUES (4, 0, 0 , 0, 0, 0, 0, false, 0, false, 0, false, false, 9);

INSERT INTO users_profile (id, numprimos,numgenesis, numgenesis, numfates, numstarglitter, character_pity, character_guaranteed, weapon_pity, weapon_guaranteed, weapon_fate_points, welkin_user, battlepass_user, user_id) VALUES (3, 0, 0 , 0, 0, 0, 0, false, 0, false, 0, false, false, 8);

INSERT INTO users_profile_banner (id, profile_id, banner_id) VALUES () ;