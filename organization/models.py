from django.core.exceptions import ValidationError
from django.db import models

from employees.models import UserProfile

"""
Models: Organization, Site, Directorate, Department, Service, Unit, CostCenter

Organization
│
└── Site
    │
    ├── Directorate
    │   │
    │   └── Department
    │       │
    │       └── Service
    │           │
    │           └── Unit
    │
    └── Department
        │
        ├── Service
        │   │
        │   └── Unit
        │
        └── Unit
"""


class CostCenter(models.Model):
    name = models.CharField(max_length=100)
    number = models.CharField(max_length=15, unique=True)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="managed_cost_centers"
    )

    controller = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="controlled_cost_centers"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return f"{self.number} - {self.name}"


class Organization(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, unique=True)
    manager = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="%(class)s_manager"
    )

    cost_center = models.ForeignKey(
        CostCenter, on_delete=models.PROTECT,
        related_name='organization_cost_centers'
    )

    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Site(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="sites"
    )

    name = models.CharField(max_length=100)
    code = models.CharField(max_length=15, unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ManagedUnit(models.Model):
    manager = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="%(class)s_manager"
    )

    deputy_manager = models.ForeignKey(
        UserProfile,
        on_delete=models.PROTECT,
        related_name="%(class)s_deputy_manager",
        null=True,
        blank=True
    )

    cost_center = models.ForeignKey(
        CostCenter, on_delete=models.PROTECT,
        related_name="%(class)s_cost_centers"
    )

    code = models.CharField(max_length=15, unique=True)
    description = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Directorate(ManagedUnit):
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="directorates"
    )

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Department(ManagedUnit):
    site = models.ForeignKey(
        Site,
        on_delete=models.PROTECT,
        related_name="direct_departments",
        null=True,
        blank=True
    )

    directorate = models.ForeignKey(
        Directorate,
        on_delete=models.PROTECT,
        related_name="departments",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)

    def clean(self):
        super().clean()

        if self.site_id and self.directorate_id:
            raise ValidationError(
                "Department cannot belong to both Site and Directorate."
            )

        if not self.site_id and not self.directorate_id:
            raise ValidationError(
                "Department must belong to either Site or Directorate."
            )

    def __str__(self):
        return self.name


class Service(ManagedUnit):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="services"
    )

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Unit(ManagedUnit):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name="direct_units",
        null=True,
        blank=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="units",
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200)

    def clean(self):
        super().clean()

        if self.department_id and self.service_id:
            raise ValidationError(
                "Unit cannot belong to both Department and Service."
            )

        if not self.department_id and not self.service_id:
            raise ValidationError(
                "Unit must belong to either Department or Service."
            )

    def __str__(self):
        return self.name




