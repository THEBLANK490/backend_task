from django.db import models
from django.contrib.gis.db.models.functions import Distance


class CustomUserManager(models.Manager):
    """
    A custom manager for the user model.

    This manager calculates the nearby_users and returns those users.
    """

    def nearby_users(self, point):
        return (
            self.filter(home_address__distance_lte=(point, 1000))
            .annotate(distance=Distance("home_address", point))
            .order_by("distance")
        )
