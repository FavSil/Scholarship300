# Scholarship300

PREVIEW https://scholarship300.herokuapp.com/archive/

favian silva
with code adapted from https://developer.mozilla.org/en-US/docs/Learn/ and youtube django tutorials


To run thiss localy for testing.

Set up a python development enivronment.
https://docs.djangoproject.com/en/2.1/howto/windows/

after python (I used 3.7)
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic
python3 manage.py createsuperuser # go through process to create a admin admin:admin password:password
python3 manage.py runserver

in browser http://127.0.0.1:8000/admin/ to open the admin site
Create a few test objects of each type.
Open tab to `http://127.0.0.1:8000/archive to see the main site, with your new objects.

to push to development after testing locally
clone the git.
while in the git directory
git add -A
git commit -m "COMMENTS"
git push ORIGIN master

download the heroku command iine
heroku username favian.silva@ucalgary.ca
password: cornmaze1$ #its a free account
 "still in git folder"
heroku push origin master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
"redo super user steaps"
heroku open
"opens site"
