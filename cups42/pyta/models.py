from django.db import models

class UserInfo(models.Model):
    name = models.CharField(max_length=64, null=True, verbose_name=u'Name')
    surname = models.CharField(max_length=64, null=True, verbose_name=u'Name')
    bio = models.TextField(null=True, verbose_name=u'BIO')
    birth_date = models.DateField(null=True, verbose_name=u'Birth date')
    contact_phone = models.CharField(max_length=64, null=True, verbose_name=u'Phone')
    contact_email = models.EmailField(max_length=128, null=True, verbose_name=u'Email')
    contact_skype = models.CharField(max_length=128, null=True, verbose_name=u'Skype')
    contact_jabber = models.EmailField(max_length=128, null=True, verbose_name=u'Jabber')
    contact_other = models.TextField(null=True, verbose_name='Other contacts')


class RequestHistoryEntry(models.Model):
    request_path = models.CharField(max_length=2048)
    request_method = models.CharField(max_length=64)
    request_time = models.DateTimeField(auto_now=True)
    
