from django.db import models

class CountryChoices(models.TextChoices):
    NEPAL = "NP"
    INDIA = "IN"
    CHINA = "CH"