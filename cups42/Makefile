test:
	python manage.py test pyta

syncdb:
	python manage.py syncdb --noinput
	python manage.py migrate pyta
	python manage.py loaddata db_data.json

run:
	python manage.py runserver
