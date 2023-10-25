from django.db.models.signals import pre_delete
from django.dispatch import receiver
from .models import Product, ProductDeletionHistory

@receiver(pre_delete, sender=Product)
def log_product_deletion(sender, instance, **kwargs):
    # Crear una instancia de ProductDeletionHistory al eliminar un producto
    ProductDeletionHistory.objects.create(product_name=instance.name, deleted_by=instance.deleted_by)
