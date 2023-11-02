from django.db import models
import shortuuid
from employee.models import Address, CustomUser
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission





class Customer(AbstractUser):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Campo de ID único
    customer_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable=False)

    # Información personal
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=[('Masculino', 'Masculino'), ('Femenino', 'Femenino'), ('Otro', 'Otro')], null=True, blank=True)
    name = models.CharField(max_length=255, null=False, blank=False)

    # CUIT/CUIL (puede ser nulo)
    cuit_cuil = models.CharField(max_length=13, unique=True, blank=True, null=True)

    # Dirección (puede ser nula)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)

    # Información de contacto
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True)
    
    
    # En el modelo Customer
    groups = models.ManyToManyField(Group, related_name='customer_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='customer_user_permissions')

    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name













    # Historial de compras
    # Aquí puedes vincular a un modelo de Pedido o Compra si lo tienes.
    # Ejemplo: compras = models.ManyToManyField('Pedido', blank=True)

    # Direcciones de envío y facturación
    # Puedes crear un modelo separado para las direcciones y vincularlo aquí.
    # Ejemplo: direcciones = models.ManyToManyField('Direccion', blank=True)

    # Tarjetas de crédito
    # Asegúrate de manejar de forma segura la información de tarjetas de crédito, 
    # esto puede implicar la encriptación de datos y el cumplimiento de PCI DSS.
    # Ejemplo: tarjetas_credito = models.ManyToManyField('TarjetaCredito', blank=True)

    # Lista de deseos
    # Ejemplo: lista_deseos = models.ManyToManyField('Producto', related_name='deseado_por', blank=True)

    # Comentarios y calificaciones
    # Ejemplo: comentarios = models.ManyToManyField('Comentario', blank=True)

    # Seguimiento de actividad
    # Ejemplo: actividad = models.ManyToManyField('Actividad', blank=True)

    # Grupos o categorías de clientes
    # Ejemplo: grupos = models.ManyToManyField('GrupoCliente', blank=True)

    # Preferencias y configuraciones
    # Puedes crear un modelo separado para esto y vincularlo aquí.
    # Ejemplo: configuracion = models.OneToOneField('ConfiguracionCliente', on_delete=models.CASCADE, null=True, blank=True)