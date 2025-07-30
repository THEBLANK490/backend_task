from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import LineString
from django.core.validators import RegexValidator

from app.users.choices import CountryChoices
from app.users.managers import CustomUserManager


class User(AbstractUser):
    country = models.CharField(max_length=100, choices=CountryChoices)
    bio = models.TextField(blank=True, null=True)
    phone_number = models.CharField(
        max_length=20,
        validators=[RegexValidator(r"^\+?1?\d{9,15}$")],
        blank=True,
        null=True,
    )
    areas_of_interest = models.JSONField(default=list)
    documents = models.FileField(upload_to="user_docs/", blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    home_address = gis_models.PointField(geography=True, blank=True, null=True)
    office_address = gis_models.PointField(geography=True, blank=True, null=True)

    objects = CustomUserManager()

    @property
    def age(self):
        if self.birthday:
            return timezone.now().date().year() - self.birthday.year

    def distance_between_locations(self):
        if self.home_address and self.office_address:
            return self.home_address.distance(self.office_address) * 100
        return None


class UserVectorLine(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    line = gis_models.LineStringField(geography=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user.home_address and self.user.office_address:
            self.line = LineString(self.user.home_address, self.user.office_address)
        super().save(*args, **kwargs)
