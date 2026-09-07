from django.contrib.auth.models import User
from django.db import models

# Models: Organization, Department, Unit, CostCenter


class Organization(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['code']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Department(models.Model):
    organization = models.ForeignKey(  # fk to Organization model
        Organization,
        on_delete=models.PROTECT,
        related_name='departments'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(  # fk to User model
        User,
        on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

        indexes = [
            models.Index(fields=["organization", "is_active"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Unit(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='units'
    )
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    indexes = [
        models.Index(fields=["department", "is_active"]),
        models.Index(fields=["name"]),
    ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class CostCenter(models.Model):
    name = models.CharField(max_length=100)
    code =models.IntegerField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name='cost_centers'
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.PROTECT,
        related_name='cost_centers'
    )

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=["organization", "is_active"]),
            models.Index(fields=["department", "is_active"]),
            models.Index(fields=["code"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"

