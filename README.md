# Backent

A Backend that stores events and their locations, and serves them using an API.

## Running Locally


```sh

$ mkvirtualenv -p /usr/bin/python3 backent
$ pip install -U pip setuptools
$ pip install -r requirements.txt

$ createdb backent

$ python manage.py migrate
$ python manage.py collectstatic
$ ENVIRONMENT=dev python manage.py runserver

```

Your app should now be running on [localhost:8000](http://localhost:8000/).

## LICENSE

MIT
