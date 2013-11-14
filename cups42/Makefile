test:
	python manage.py test pyta

syncdb:
	python manage.py syncdb --noinput
	python manage.py schemamigration pyta --initial
	python manage.py migrate pyta --fake
