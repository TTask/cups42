from django.core.management.base import BaseCommand, CommandError
from django.db.models import get_app
from django.db.models import get_models
from django.core.exceptions import ImproperlyConfigured


class Command(BaseCommand):
    '''show all models in specified app'''
    args = 'application name'
    help = 'Show the list of models and model objects count in specified app'

    def handle(self, *args, **options):
        try:
            app = get_app(args[0])
        except IndexError:
            raise CommandError("Command needs 1 argument, 0 given")
        except ImproperlyConfigured:
            raise CommandError("App with name %s could not be found" % args[0])
        for model in get_models(app):
            model_count = model.objects.count()
            message = """MODEL %s has:
                %d objects in db\n""" % (str(model.__name__),
                                         model_count)
            self.stdout.write(message)
            self.stderr.write("error:\t%s" % message)
