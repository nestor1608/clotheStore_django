from django.db import models
from django.contrib.auth.models import AbstractUser
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
    id_employee = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name='employee_addresses')
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

class CustomUser(AbstractUser):
    ROL_CHOICES = (
        ('superuser', 'Superuser'),
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('customer', 'Customer'),
    )
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default='customer')
    # En el modelo CustomUser
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')



class Employee(AbstractUser):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(Address, related_name='direccion', on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], null=True, blank=True)
    dni = models.CharField(max_length=128, unique=True)  # Asumimos un máximo de 128 caracteres para el hash
    email = models.EmailField()
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, null=True, blank=True)
    hire_date = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # En el modelo Employee
    groups = models.ManyToManyField(Group, related_name='employee_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='employee_user_permissions')
    
    # Registration Date (Creation Date)
    created_at = models.DateTimeField(auto_now_add=True)

    # Update Date (Last Modification Date)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pk} - {self.first_name} {self.last_name} - {self.position}"



class Manager(Employee):
    pass
    # Agrega campos adicionales para el gerente









