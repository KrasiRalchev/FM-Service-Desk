from django.db import models


class AssetType_choices(models.TextChoices):
    FACILITY = "FACILITY", "Facility"
    BUILDING = "BUILDING", "Building"
    ROAD = "ROAD", "Road"
    VEHICLE = "VEHICLE", "Vehicle"
    OTHER = "OTHER", "Other"

