blog
====

tl;dr:
A flask and mongoengine backed web-app for note-taking, whether it is TODO list, article or simple reminder.

Installation
------------

Pre-requisite: have mongodb installed -- in ubuntu:
````
sudo apt-get install mongodb
````
### Using pyvenv

Setting-up the virtualenv (creates a virtualenv called '.venv' -- the resulting .venv folder will be hidden in linux --, ignored by git (cf .gitignore))
````
pyvenv ./.venv
````

Activate your newly created virtualenv:
````
source ./.venv/bin/activate
````

To deactivate the virtual environment, simply:
````
deactivate
````

### Using conda:
Again, we are createing a virualenv called venv.
````
conda create --name venv
````

To activate your new environment:
````
source activate venv
````

To desactivate it:
````
source deactivate
````


### Get all the requirements:
````
pip3 install -r requirements.txt
````

Usage
-----

Initialise the db:
````
python manage.py init
````

Run the test server:
````
python manage.py runserver
````

The app
-------

All posts (default article, todo list, etc) can be public or private.
Private items (and public ones) can be accessed through ```/post/list``` whereas public ones are listed at ````/blog````.
