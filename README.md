# cpmisfacerecognition

Solving the photo search and photo progression challenge.

Usage
To use this template to start your own project:

Existing virtualenv
If your project is already in an existing python3 virtualenv first install django by running

$ pip install django
And then run the django-admin.py command to start the new project:

$ django-admin.py startproject \
  
No virtualenv
This assumes that python3 is linked to valid installation of python 3 and that pip is installed and pip3is valid for installing python 3 packages.

Installing inside virtualenv is recommended, however you can start your project without virtualenv too.

If you don't have django installed for python 3 then run:

$ pip3 install django
And then:

$ python3 -m django startproject \

After that just install the local dependencies, run migrations, and start the server.

Getting Started
First clone the repository from Github and switch to the new directory:

$ git clone git@github.com/USERNAME/{{ project_name }}.git
$ cd {{ project_name }}
Activate the virtualenv for your project.

Install project dependencies:

$ pip install -r requirements/local.txt
Then simply apply the migrations:

$ python manage.py migrate
You can now run the development server:

$ python manage.py runserver
