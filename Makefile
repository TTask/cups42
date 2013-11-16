test:
	python manage.py test pyta

syncdb:
	python manage.py syncdb --noinput --migrate

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups42.settings manage.py runserver