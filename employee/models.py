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


class AddressEmployee(models.Model):
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
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.ForeignKey(AddressEmployee, related_name='direccion', on_delete=models.CASCADE)
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

    def check_today_entry(self):
        today = date.today()
        entries_today = EntryRecord.objects.filter(employee=self, entry_date__date=today)
        return entries_today.exists()
    
    def set_dni(self, raw_dni):
        self.dni = make_password(raw_dni)


class EntryRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    entry_date = models.DateTimeField(auto_now_add=True)
    exit_date = models.DateTimeField(null=True, blank=True)
    # Registration Date (Creation Date)
    created_at = models.DateTimeField(auto_now_add=True)

    # Update Date (Last Modification Date)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.exit_date and self.exit_date < self.entry_date:
            raise ValidationError("Exit date cannot be earlier than entry date.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.first_name} - Entry: {self.entry_date} - Exit: {self.exit_date}"

class DisciplineRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    discipline_date = models.DateField()
    discipline_reason = models.CharField(max_length=255)
    justified = models.BooleanField(default=False)
    # Registration Date (Creation Date)
    created_at = models.DateTimeField(auto_now_add=True)

    # Update Date (Last Modification Date)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Discipline record for {self.employee.username} on {self.discipline_date}"

def check_late_arrival(employee_id, current_time):
    try:
        entry_schedule = EntrySchedule.objects.get(employee_id=employee_id)
        if current_time > entry_schedule.entry_time:
            discipline_reason = f"Late arrival due to... " # add subtraction {entry_schedule -  }
            discipline_date = datetime.now().date()
            DisciplineRecord.objects.create(employee=employee_id, discipline_date=discipline_date, discipline_reason=discipline_reason)
    except EntrySchedule.DoesNotExist:
        pass
    
class EntrySchedule(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    entry_time = models.TimeField()
    exit_time = models.TimeField()
    # Registration Date (Creation Date)
    created_at = models.DateTimeField(auto_now_add=True)

    # Update Date (Last Modification Date)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Entry schedule for {self.employee.username} at {self.entry_time}"


