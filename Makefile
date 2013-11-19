test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups42.settings python manage.py test pyta

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups42.settings python manage.py syncdb
	python manage.py migrate pyta
	python manage.py loaddata db_data.json

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups42.settings python manage.py runserver
