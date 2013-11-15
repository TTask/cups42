from django.db import models
from sorl.thumbnail import ImageField


class UserInfo(models.Model):
    photo = ImageField(blank=True, null=True, upload_to="user_media/photo/", verbose_name=u'Photo')
    name = models.CharField(blank=True, max_length=64, null=True, verbose_name=u'Name')
    surname = models.CharField(blank=True, max_length=64, null=True, verbose_name=u'Surname')
    bio = models.TextField(blank=True, null=True, verbose_name=u'BIO')
    birth_date = models.DateField(blank=True, null=True, verbose_name=u'Birth date')
    contact_phone = models.CharField(blank=True, max_length=64, null=True, verbose_name=u'Phone')
    contact_email = models.EmailField(blank=True, max_length=128, null=True, verbose_name=u'Email')
    contact_skype = models.CharField(blank=True, max_length=128, null=True, verbose_name=u'Skype')
    contact_jabber = models.EmailField(blank=True, max_length=128, null=True, verbose_name=u'Jabber')
    contact_other = models.TextField(blank=True, null=True, verbose_name='Other contacts')


class RequestHistoryEntry(models.Model):
    request_path = models.CharField(max_length=2048)
    request_method = models.CharField(max_length=64)
    request_time = models.DateTimeField(auto_now=True)
    
