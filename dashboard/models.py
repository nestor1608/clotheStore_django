from django.db import models

# Create your models here.
from django.contrib.auth.models import User



class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('jefe', 'Jefe'),
        ('empleado', 'Empleado'),
        ('developer', 'Developer (dyel master)'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.user.username