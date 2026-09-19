from django.db import models


class Site_choices(models.TextChoices):
    VARNA = "varna", "VARNA"
    BURGAS = "burgas", "BURGAS"