from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Product
from stock.models import StockProduct
from customers.models import Customer
from employee.models import Employee
import shortuuid


class Sale(models.Model):
    sale_id = models.CharField(max_length=11, unique=True, default=shortuuid.uuid, editable= False)
    date_sale = models.DateTimeField(auto_now_add=True)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_realizadas')
    cliente = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_realizadas')
    importe_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Venta {self.sale_id} - {self.date_sale}"
    
class ItemSale(models.Model):
    id_sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='item_sales')
    price_unit = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def price_unit(self):
        return self.id_product.price_sale
    
    def subtotal(self):
        return self.id_product.price_sale * self.cantidad

@receiver(post_save, sender=ItemSale)
def check_stock(sender, instance, **kwargs):
    product = instance.id_product

    try:
        stock = StockProduct.objects.get(id_product = product.id_product)
        stock_now = stock.amount_stock

        if stock_now < stock.amount_min_desirable:
            print(f"ALERTA: El producto '{product.id_product.name}' tiene una cantidad en stock menor a 5 (Stock actual: {stock_now}).")
    except StockProduct.DoesNotExist:
        print(f"ADVERTENCIA: No se encontró información de stock para el producto '{product.id_product.name}'.")

