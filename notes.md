user portion from:
<https://dev.to/earthcomfy/creating-a-django-registration-login-app-part-i-1di5>

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

python manage.py dumpdata analyze.character > characters.json
python manage.py dumpdata analyze.banner analyze.characterbanner analyze.weaponbanner > banners.json

python manage.py makemigrations
python manage.py sqlmigrate
python manage.py migrate
python manage.py runserver

python manage.py shell

python manage.py test analyze

# PYTEST NOTES

coverage run -m pytest
coverage report -m

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

# DJANGO

DJANGO GENERIC VIEWS

DJANGO GENERIC VIEWS
DJANGO GENERIC VIEWS
DJANGO GENERIC VIEWS
DJANGO GENERIC VIEWS
<https://docs.djangoproject.com/en/4.1/topics/class-based-views/>

<https://docs.djangoproject.com/en/4.1/intro/tutorial02/>
\ to run it in browser
python manage.py runserver 8080

\ apps are like analytical vs wish proj vs wish sim
python manage.py startapp appnamehere

\ updates the databse or something, use when you change models for sure
python manage.py migrate
\ when altering models?
python manage.py makemigrations polls
\ takes migration and returns sql
python manage.py sqlmigrate polls 0001

\ add apps to installed apps from your made ones:
INSTALLED_APPS  = ['myapp.apps.myappConfig', ...]

\ use admin.py to make the models modifiable in the admin website
\ use <http://127.0.0.1:8000/admin/> to access the admin website

"The default settings file configures a DjangoTemplates backend whose APP_DIRS option is set to True
By convention DjangoTemplates looks for a “templates” subdirectory in each of the INSTALLED_APPS."

- idk what this means

template:
polls/templates/polls/index.html -> polls/index.html
can be referred to as the latter if the filepath is the former

"However, since you defined the name argument in the path() functions in the polls.urls module, you can remove a reliance on specific URL paths defined in your url configurations by using the {% url %} template tag"
this:
<li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>
better than this for some reason:
<li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
and then this is even better:
<li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>

but you have to add the app name (in this case 'polls')

"We set the form’s action to {% url 'polls:vote' question.id %}, and we set method="post". Using method="post" (as opposed to method="get") is very important, because the act of submitting this form will alter data server-side. Whenever you create a form that alters data server-side, use method="post". This tip isn’t specific to Django; it’s good web development practice in general."

"After incrementing the choice count, the code returns an HttpResponseRedirect rather than a normal HttpResponse. HttpResponseRedirect takes a single argument: the URL to which the user will be redirected (see the following point for how we construct the URL in this case).

As the Python comment above points out, you should always return an HttpResponseRedirect after successfully dealing with POST data. This tip isn’t specific to Django; it’s good web development practice in general."

Convert the URLconf.
Delete some of the old, unneeded views.
Introduce new views based on Django’s generic views.

Python has been installed as
  /usr/local/bin/python3

You can install Python packages with
  pip3 install <package>
They will install into the site-package directory
  /usr/local/lib/python3.10/site-packages

If you need to have curl first in your PATH, run:
  echo 'export PATH="/usr/local/opt/curl/bin:$PATH"' >> ~/.zshrc

<https://www.selenium.dev/>
?

style css
