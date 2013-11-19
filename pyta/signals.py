from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from models import ModelHistoryEntry


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
