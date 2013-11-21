from django.db import models
from sorl.thumbnail import ImageField
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver


class UserInfo(models.Model):
    photo = ImageField(blank=True, null=True,
                       upload_to="user_media/photo/",
                       verbose_name=u'Photo')
    name = models.CharField(max_length=64, null=True,
                            verbose_name=u'Name')
    surname = models.CharField(max_length=64, null=True,
                               verbose_name=u'Surname')
    bio = models.TextField(null=True, verbose_name=u'BIO')
    birth_date = models.DateField(null=True,
                                  verbose_name=u'Birth date')
    contact_phone = models.CharField(max_length=64, null=True,
                                     verbose_name=u'Phone')
    contact_email = models.EmailField(max_length=128, null=True,
                                      verbose_name=u'Email')
    contact_skype = models.CharField(max_length=128, null=True,
                                     verbose_name=u'Skype')
    contact_jabber = models.EmailField(max_length=128, null=True,
                                       verbose_name=u'Jabber')
    contact_other = models.TextField(blank=True, null=True,
                                     verbose_name='Other contacts')

    def __unicode__(self):
        return unicode("%s %s" % (self.name,
                                  self.surname))

    def repr(self):
        return "%s %s" % (self.name, self.surname)

    def attrDict(self):
        attribute_dict = {}
        for attr, value in self.__dict__.iteritems():
          if not attr.startswith('_') and attr != 'id':
            attribute_dict[str(attr)] = str(value)
        return attribute_dict


class RequestHistoryEntry(models.Model):
    request_path = models.CharField(max_length=2048)
    request_method = models.CharField(max_length=64)
    request_time = models.DateTimeField(auto_now=True)
    request_priority = models.IntegerField(default=0)

    def __unicode__(self):
        return unicode("%s %s" % (
            self.request_path,
            self.request_method))

    def repr(self):
        return "%s %s" % (self.request_path, self.request_method)


class ModelHistoryEntry(models.Model):
    model_name = models.CharField(max_length=256)
    change_type = models.CharField(max_length=128)
    change_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode("%s has %s" % (self.model_name, self.change_type))

    def repr(self):
        return "%s %s" % (self.model_name, self.change_type)


class RequestPriorityEntry(models.Model):
  request_path = models.CharField(max_length=2048,
                                  verbose_name="Request path")
  request_priority = models.IntegerField(default=0,
                                        verbose_name="Priority")


#-----------------------------------------------------------------------------#
#                                SIGNAL PROCESSORS                            #
#-----------------------------------------------------------------------------#
@receiver(post_save)
def save_handler(sender, **kwargs):
    if not sender.__name__ == ModelHistoryEntry.__name__:
        try:
            if kwargs['created']:
                ModelHistoryEntry.objects.create(
                    model_name=sender.__name__,
                    change_type="CREATED")

            else:
                ModelHistoryEntry.objects.create(
                    model_name=sender.__name__,
                    change_type="MODIFIED")
        except:
            return


@receiver(post_delete)
def delete_handler(sender, **kwargs):
    try:
        ModelHistoryEntry.objects.create(
            model_name=sender.__name__,
            change_type="DELETED")
    except:
        return

