from django.db import models

from facilities.choices import AssetType_choices
from organization.models import CostCenter

# Models: Facility


# Site
#  └── Building
#       └── Floor
#            └── Area
#
# Asset
#  ├── Building
#  ├── Vehicle
#  ├── Equipment
#  ├── Facility
#  └── ...
#
# Road
#  └── RoadSegment


class Site(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)

    address = models.CharField(max_length=300, blank=True)
    city = models.CharField(max_length=100, blank=True)

    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.PROTECT,
        related_name="sites",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["city"]),
            models.Index(fields=["is_active"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Building(models.Model):
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="buildings",
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    address = models.CharField(max_length=300, blank=True)

    floors_count = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    total_area = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
    )

    construction_year = models.PositiveIntegerField(
        null=True,
        blank=True,
    )

    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.PROTECT,
        related_name="buildings",
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["site", "code"],
                name="unique_building_code_per_site",
            ),
        ]

        indexes = [
            models.Index(fields=["site", "is_active"]),
            models.Index(fields=["name"]),
            models.Index(fields=["cost_center"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Floor(models.Model):
    building = models.ForeignKey(
        Building,
        on_delete=models.PROTECT,
        related_name="floors",
    )

    name = models.CharField(max_length=100)
    number = models.IntegerField()

    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["number"]

        constraints = [
            models.UniqueConstraint(
                fields=["building", "number"],
                name="unique_floor_per_building",
            ),
        ]

    def __str__(self):
        return f"{self.building} - {self.name}"


class Area(models.Model):
    floor = models.ForeignKey(
        Floor,
        on_delete=models.PROTECT,
        related_name="areas",
    )

    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50)

    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

        constraints = [
            models.UniqueConstraint(
                fields=["floor", "code"],
                name="unique_area_code_per_floor",
            ),
        ]

        indexes = [
            models.Index(fields=["floor"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


#

class Asset(models.Model):
    asset_number = models.CharField(
        max_length=50,
        unique=True,
    )

    name = models.CharField(max_length=200)

    asset_type = models.CharField(
        max_length=30,
        choices=AssetType_choices.choices, default=AssetType_choices.FACILITY
    )

    description = models.TextField(blank=True)

    location = models.ForeignKey(
        Area,
        on_delete=models.PROTECT,
        related_name="assets",
        null=True,
        blank=True,
    )

    cost_center = models.ForeignKey(
        CostCenter,
        on_delete=models.PROTECT,
        related_name="assets",
        null=True,
        blank=True,
    )

    manufacturer = models.CharField(
        max_length=200,
        blank=True,
    )

    model = models.CharField(
        max_length=200,
        blank=True,
    )

    serial_number = models.CharField(
        max_length=200,
        blank=True,
    )

    purchase_date = models.DateField(
        null=True,
        blank=True,
    )

    commissioning_date = models.DateField(
        null=True,
        blank=True,
    )

    warranty_until = models.DateField(
        null=True,
        blank=True,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["asset_number"]

        indexes = [
            models.Index(fields=["asset_type", "is_active"]),
            models.Index(fields=["location"]),
            models.Index(fields=["cost_center"]),
            models.Index(fields=["manufacturer"]),
            models.Index(fields=["serial_number"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.asset_number} - {self.name}"