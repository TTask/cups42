
def settings_context(request):
    from django.conf import settings
    return {'django_settings': settings}
