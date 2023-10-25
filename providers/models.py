from django.db import models
import shortuuid

class Providers(models.Model):
    provider_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable=False)
    bussines_name = models.CharField(max_length=100, blank=True, null=True)
    cuit_cuil = models.CharField(max_length=13, unique=True, blank=True, null=True)
    product = models.ManyToManyField('products.Product', related_name='proveedores', blank=True)
    sector = models.CharField(max_length=20, blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.bussines_name

class Seller(models.Model):
    seller_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable=False)
    id_provider = models.ForeignKey(Providers,on_delete=models.SET_NULL, null=True, blank=True)
    seller_name = models.CharField(max_length=100, blank=True, null=True)
    telefon = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null= True)
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 


