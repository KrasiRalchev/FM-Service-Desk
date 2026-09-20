from django.db import models


class Site_choices(models.TextChoices):
    VARNA = "VAR", "VAR"
    BURGAS = "BOJ", "BOJ"


class Department_choices(models.TextChoices):
    FACILITY_MANAGEMENT = "Facility Management", "Facility Management"
    PROCUREMENT = "Procurement", "Procurement"
    ACCOUNTANT = "Accountant", "Accountant"
    TERMINAL_MANAGEMENT = "Terminal Management", "Terminal Management"
    APRON_SERVICES = "Apron Services", "Appron Services"
    PASSENGER_SERVICES = "Passenger Services", "Passenger Services"
    HUMAN_RESOURCES = "Human Resources", "Human Resources"
    SECURITY = "Security", "Security"
    SAFETY = "Safety", "Safety"
    AOC = "AOC", "AOC"
    IT = "IT", "IT"

