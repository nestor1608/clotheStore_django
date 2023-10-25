from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group,User
from .models import Employee
import secrets
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password


def generate_random_password():
    # Genera una contraseña aleatoria de 8 caracteres
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    password = ''.join(secrets.choice(alphabet) for i in range(8))
    return password



@receiver(post_save, sender=Employee)
def assign_employee_role(sender, instance, created, **kwargs):
    if created:
        # Asigna el rol de "empleado" al usuario
        employee_group = Group.objects.get(name='employee')  # Asegúrate de que el grupo "employee" exista
        instance.groups.add(employee_group)

        # Genera el nombre de usuario basado en el nombre y los últimos 3 números del DNI (o el email)
        # Aquí, asumimos que el DNI se almacena en un campo llamado 'dni' en el modelo Employee
        dni = instance.dni  # Asegúrate de que este campo exista o ajústalo según tu modelo
        username = f"{instance.first_name.lower()}{instance.last_name.lower()}{dni[-3:]}"
        
        # Verifica si el nombre de usuario ya existe y agrega un número al final si es necesario
        i = 1
        while User.objects.filter(username=username).exists():
            username = f"{instance.first_name.lower()}{instance.last_name.lower()}{dni[-3:]}{i}"
            i += 1

        instance.username = username
        
        # Genera y establece una contraseña aleatoria
        password = generate_random_password()
        instance.set_password(password)

        # Guarda los cambios en el modelo Employee
        instance.save()

        # Envía la contraseña al empleado por correo electrónico
        send_password_email(instance, password)

def send_password_email(employee, password):
    subject = 'Contraseña de su cuenta'
    message = f'Su contraseña temporal es: {password}. Cambie su contraseña después de iniciar sesión.'
    from_email = 'nestor.268@Outlook.com'  # Ajusta esto según tu configuración de correo
    recipient_list = [employee.email]  # Suponemos que el empleado tiene un campo "email"

    send_mail(subject, message, from_email, recipient_list)
