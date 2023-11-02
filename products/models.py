from django.db import models
from django.contrib.auth.models import User
from providers.models import Providers
import shortuuid
from django.core.exceptions import ValidationError

class Category(models.Model):

    name = models.CharField(max_length=50)
    
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SubCategory(models.Model):
    
    associated_category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)

    name = models.CharField(max_length=50)

    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class ProductDataGeneral(models.Model):
    product_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable= False)
    name = models.CharField(max_length=100)
    img = models.ImageField(upload_to='media/product')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    
    sub_category = models.ForeignKey(SubCategory, on_delete=models.DO_NOTHING)
    brand = models.CharField(max_length=50, blank=True, null=True) 
    
    provider = models.ManyToManyField(Providers, blank=True, related_name='provider')
    
    number_serie = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    
    # persona que realiza la carga del producto
    user_create_price = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable= False)
    
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.product_id} - {self.name}'

# ------------------ VARIABLES QUE DETERMINAN EL PRECIO DE VENTA -----------------------

class ValuesPriceProduct(models.Model):
    id_product = models.ForeignKey(ProductDataGeneral, on_delete=models.CASCADE)
    
    # precio del proveedor
    price_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # precio real con costos
    real_price_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    
    # margen de ganancia precio unitario
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2, default=0.21, blank=True, null=True)
    
    # precio sugerido  
    suggested_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # precio de mercado
    market_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # precio anterior
    last_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # descuento
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    
    # precio por mayor
    price_wholesale = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)  
    
    # precio con descuento
    price_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # precio de venta
    price_sale = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id_product

    def clean(self):
        # Validación personalizada: El precio de venta no debe ser menor que el precio de compra
        if self.price_sale is not None and self.price_cost is not None and self.price_sale < self.price_cost:
            raise ValidationError("El precio de venta no puede ser menor que el precio de compra.")
        


# ----------------- COSTO DE PRODUCTO --------------------------------

class ProductCost(models.Model):
    id_product = models.ForeignKey(ProductDataGeneral, on_delete=models.DO_NOTHING)
    product_cost_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable= False)
    amount_total_percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)

class ItemProductCost(models.Model):
    id_product_cost = models.ForeignKey(ProductCost, on_delete= models.CASCADE)
    description_cost = models.CharField(max_length=100)
    amounts_cost = models.DecimalField(max_digits=5, decimal_places=2, default=0, blank=True, null=True)
    add_price = models.BooleanField(default=True)


