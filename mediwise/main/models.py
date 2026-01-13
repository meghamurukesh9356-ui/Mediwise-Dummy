from django.db import models

# Create your models here.

class Users(models.Model):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
        ('pharmacist', 'Pharmacist'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    id = models.AutoField(primary_key=True)

    def __str__(self):
        return f"{self.role} {self.id}"

class MediAdmin(models.Model):
    id = models.BigAutoField(primary_key=True)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=100)

class Patient(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True)
    BLOOD_GROUP_CHOICES = (
        ('o+', 'O+'),
        ('o-', 'O-'),
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
    )
    blood_group = models.CharField(max_length=20, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    height = models.CharField(max_length=10, null=True, blank=True)
    weight = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Pharmacist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES)
    license_number = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    address = models.TextField()
    registration_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
