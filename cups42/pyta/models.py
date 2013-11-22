from django.db import models
from sorl.thumbnail import ImageField


class UserInfo(models.Model):
    photo = ImageField(blank=True,
                       upload_to="user_media/photo/",
                       verbose_name='Photo')
    name = models.CharField(max_length=64,
                            null=True,
                            verbose_name='Name')
    surname = models.CharField(max_length=64,
                               null=True,
                               verbose_name='Surname')
    bio = models.TextField(null=True, verbose_name='BIO')
    birth_date = models.DateField(null=True, verbose_name='Birth date')
    contact_phone = models.CharField(max_length=64,
                                     null=True,
                                     verbose_name='Phone')
    contact_email = models.EmailField(max_length=128,
                                      null=True,
                                      verbose_name='Email')
    contact_skype = models.CharField(max_length=128,
                                     null=True,
                                     verbose_name='Skype')
    contact_jabber = models.EmailField(max_length=128,
                                       null=True,
                                       verbose_name='Jabber')
    contact_other = models.TextField(null=True,
                                     verbose_name='Other contacts')


class RequestHistoryEntry(models.Model):
    request_path = models.CharField(max_length=2048)
    request_method = models.CharField(max_length=64)
    request_time = models.DateTimeField(auto_now=True)
