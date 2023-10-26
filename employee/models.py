from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, date
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

# Solución para 'auth.User'
User.add_to_class(
    'custom_groups',
    models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='auth_users')
)
# Solución para 'auth.User'
User.add_to_class(
    'custom_user_permissions',
    models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='auth_users')
)


class Address(models.Model):
    id_employee = models.ForeignKey('Employee', on_delete=models.CASCADE)
    street = models.CharField(max_length=255, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True, verbose_name='provincia/estado')
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100)

    # Campos adicionales opcionales
    complement = models.CharField(max_length=255, blank=True, null=True)
    referent = models.TextField(blank=True, null=True)


    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.street}, {self.town}, {self.province}, {self.country}'

class Employee(AbstractUser):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, related_name='direccion', on_delete=models.CASCADE)
    dni = models.CharField(max_length=128, unique=True)  # Asumimos un máximo de 128 caracteres para el hash
    email = models.EmailField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name='employee_groups'  # Puedes usar cualquier nombre descriptivo aquí
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name='employee_user_permissions'  # Puedes usar cualquier nombre descriptivo aquí
    )
    # Registration Date (Creation Date)
    created_at = models.DateTimeField(auto_now_add=True)

    # Update Date (Last Modification Date)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} - {self.first_name} {self.last_name} - {self.position}"


class Cliente(Employee):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Agrega campos adicionales para el cliente

class Gerente(Employee):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Agrega campos adicionales para el gerente


class Empleado(Employee):
    user = models.OneToOneField(User, on_delete=models.CASCADE)









