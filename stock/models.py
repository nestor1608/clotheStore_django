from django.db import models
from products.models import Product
import shortuuid
from django.core.exceptions import ValidationError
# Create your models here.


class StockProduct(models.Model):
    stock_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable= False)
    id_product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='stock_product' )
    amount_stock = models.DecimalField(max_digits=10, decimal_places=2)
    amount_show = models.DecimalField(max_digits=10, decimal_places=2)
    amount_deposit = models.DecimalField(max_digits=10, decimal_places=2)
    amount_min_desirable = models.DecimalField(max_digits=10, decimal_places=2)
    # Fecha de registro (fecha de creación)
    created_at = models.DateTimeField(auto_now_add=True)

    # Fecha de actualización (fecha de última modificación)
    updated_at = models.DateTimeField(auto_now=True)
    
    def clean(self):
        if self.amount_show + self.amount_deposit > self.amount_stock:
            raise ValidationError("La suma de amount_show y amount_deposit no puede ser mayor que amount_stock.")
        
    def __str__(self):
        return 


