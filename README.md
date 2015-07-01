blog
====

tdlr:
A flask and mongoengine backed web-app for note-taking, whether it is TODO list, article or simple reminder.

Installation
------------

Pre-requisite: have mongodb installed -- in ubuntu:
```
sudo apt-get install mongodb
```

Setting-up the virtualenv (creates a virtualenv called venv, ignored by git (cf .gitignore))
```
pyvenv ./venv
```

Activate your newly created virtualenv:
```
source activate venv/bin/activate
```

Get all the requirements:
```
pip3 install -r requirements.txt
```

Usage
-----

Initialise the db:
```
python manage.py init
```

Run the test server:
```
python manage.py runserver
```
