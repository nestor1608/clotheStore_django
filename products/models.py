from django.db import models
from django.contrib.auth.models import User
from providers.models import Providers
import shortuuid
from django.core.exceptions import ValidationError

class Category(models.Model):
    category_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable= False)
    name = models.CharField(max_length=50)
    
    # admite venta por kilo?
    supports_sales_by_kilograms = models.BooleanField(default=False)
    
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    

class ProductDataGeneral(models.Model):
    product_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable= False)
    name = models.CharField(max_length=100)
    imagen_url = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    brand = models.CharField(max_length=50, blank=True, null=True) 
    
    provider = models.ManyToManyField(Providers, blank=True, related_name='provider')
    
    number_serie = models.CharField(max_length=100, blank=True, null=True)

    description = models.TextField(blank=True, null=True)
    
    expiration_date = models.DateField(blank=True, null=True)

    # persona que realiza la carga del producto
    user_create_price = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable= False)
    
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name

# ------------------ VARIABLES QUE DETERMINAN EL PRECIO DE VENTA -----------------------

class ValuesPriceProduct(models.Model):
    id_product = models.ForeignKey(ProductDataGeneral, on_delete=models.CASCADE)
    
    # precio del proveedor
    price_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # precio real con costos
    real_price_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
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
    
    #precio por mayor
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
        

class ValuesPriceProductforKgorMt(models.Model):
    UNIT_CHOICES = [
    ('kg', 'Kilogramos'),
    ('m', 'Metros'),
    ]
    id_product = models.ForeignKey(ProductDataGeneral, on_delete=models.CASCADE)
    
    
    # eleccion de unidad de medida
    unit_of_measurement = models.CharField(max_length=2, choices=UNIT_CHOICES)
    
    # cantidad de kilos o metros
    amount_by = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # precio por unidad
    price_unit_measure = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    
    # precio del proveedor
    price_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # precio real con costos
    real_price_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
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
    
    #precio por mayor
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
    
    def save(self, *args, **kwargs):
        if self.unit_of_measurement == 'kg':
            self.price_unit_measure = self.real_price_cost / self.amount_by
            
        elif self.unit_of_measurement == 'm':
            self.price_unit_measure = self.real_price_cost / self.amount_by  # Ajusta esto según tus necesidades
        super(ValuesPriceProductforKgorMt, self).save(*args, **kwargs)


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


# ------------------------------- HISTORIAL DE COSTO -------------------------

class CostHistory(models.Model):
    id_product_cost = models.ForeignKey(ProductCost, on_delete= models.CASCADE)
    # precio del proveedor
    amount_cost = models.DecimalField(max_digits=4, decimal_places=3, default=0, blank=True, null=True)

    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)
    
    
class ItemProductCostHistory(models.Model):
    id_item_product_cost = models.ForeignKey(ItemProductCost, on_delete=models.CASCADE)
    date_changed = models.DateTimeField(auto_now_add=True)
    new_amounts_cost = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    new_percentage_on_sales_price = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)

# ----------------------------- HISTORIAL DE PRECIO -----------------------------------

class ProductPriceHistory(models.Model):

    id_product = models.ForeignKey(ProductDataGeneral, on_delete=models.DO_NOTHING, db_index=True)
    # persona que realizo el cambio de precio 
    user_change_price = models.ForeignKey(User,on_delete=models.DO_NOTHING, editable= False)
    # precio del proveedor
    price_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # precio de venta
    price_sale = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, null=True)
    
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id_product} - {self.id_product.name} - {self.created_at}'
    


#------------------------------- HISTORIAL DE ELIMINACION ---------------------

class ProductDeletionHistory(models.Model):
    product_name = models.CharField(max_length=100)
    deleted_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable= False)
    deletion_date = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'{self.product_name} eliminado por {self.deleted_by} el {self.deletion_date}'
