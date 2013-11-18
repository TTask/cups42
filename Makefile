test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups42.settings python manage.py test pyta

syncdb:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups42.settings python manage.py syncdb --noinput --migrate

run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups42.settings python manage.py runserver