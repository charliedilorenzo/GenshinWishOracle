# PYTEST NOTES

coverage run -m pytest
coverage report -m

# GIT NOTES

git rm --cached .gitignore

# VirtualEnv NOTES

C:\Users\carol\AppData\Local\Programs\Python\Python39\python.exe

virtualenv --python  venv

.\venv\Scripts\activate

deactivate

pip freeze > requirements.txt

pip install -r requirements.txt

# DJANGO

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
