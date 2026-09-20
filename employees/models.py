from django.db import models
from django.contrib.auth.models import User

from cloudinary.models import CloudinaryField

from employees.choices import Site_choices, Department_choices


# Models: UserProfile

class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    site = models.CharField(max_length=50, choices=Site_choices.choices)
    position = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, choices=Department_choices.choices)
    phone = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20, blank=True)

    profile_photo = CloudinaryField(
        'profile_photo',
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"