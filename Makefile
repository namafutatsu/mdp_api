PROJECT := backent


clean:
	rm -rf $(PROJECT)/staticfiles
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete


setup: update resetdb

prepare:
	python manage.py migrate --noinput
	python manage.py collectstatic --noinput

serve: prepare
	python manage.py runserver


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


resetdb: initdb
	./manage.py migrate
	./manage.py loaddata initial-fixture.json

reload_db: initdb
	psql -d backent < scripts/reload_me.sql

reset_test:
	SECRET_KEY=caca ENVIRONMENT=dev python manage.py test

test:
	SECRET_KEY=caca ENVIRONMENT=dev python manage.py test --keepdb
