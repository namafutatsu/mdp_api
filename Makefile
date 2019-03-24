PROJECT ?= mdp_api
PREFIX ?= ENVIRONMENT=dev SECRET_KEY=caca MEDIA_ROOT=backups/media 


clean:
	rm -rf mdp_api/staticfiles
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete


setup: update resetdb

prepare:
	$(PREFIX) python manage.py migrate --noinput
	$(PREFIX) python manage.py collectstatic --noinput

serve: prepare
	$(PREFIX) python manage.py runserver


update:
	pip install -U pip setuptools
	pip install -e .
	pip install -r requirements_dev.txt


pylint:
	pylint --rcfile=.pylintrc $(PROJECT)


initdb:
	dropdb --if-exists $(PROJECT)
	createdb $(PROJECT)
	psql -c "CREATE EXTENSION POSTGIS;" $(PROJECT)


resetdb: initdb prepare

reset_test:
	$(PREFIX) python manage.py test

test:
	$(PREFIX) python manage.py test --keepdb
