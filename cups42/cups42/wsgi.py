"""
<<<<<<< HEAD
WSGI config for cups42 project.
=======
WSGI config for adminfor project.
>>>>>>> t1_show_user_info

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
<<<<<<< HEAD
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cups42.settings")
=======
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "adminfor.settings")
>>>>>>> t1_show_user_info

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
