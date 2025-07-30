from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.gis.geos import LineString

from app.users.models import User, UserVectorLine


@receiver(post_save, sender=User)
def update_vector_line(sender, instance, **kwargs):
    """
    A signal to create or update the users vector line.
    """
    if instance.home_address and instance.office_address:
        UserVectorLine.objects.update_or_create(
            user=instance,
            defaults={
                "line": LineString(instance.home_address, instance.office_address)
            },
        )
