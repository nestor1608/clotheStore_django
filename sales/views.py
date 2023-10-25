
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.db import transaction

from django.contrib.auth.models import User
from .models import Sale, ItemSale
from products.models import Product


class SaleView(CreateView):
    model = Sale
    fields = ['cliente', 'importe_total']  # Campos del modelo Sale que se mostrarán en el formulario
    template_name = 'ventas/venta.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.employee = self.request.user
            self.object = form.save()
            
            # Crea automáticamente los elementos relacionados en ItemSale
            for product in Product.objects.all():  # Supongamos que tienes un modelo Product para obtener todos los productos
                item_sale = ItemSale(
                    id_sale=self.object,
                    id_product=product,
                    price_unit=product.price_sale,  # Asegúrate de obtener el precio del producto de alguna manera
                    cantidad=1  # Cantidad inicial
                )
                item_sale.subtotal = item_sale.price_unit * item_sale.cantidad  # Calcula el subtotal
                item_sale.save()

        return super().form_valid(form)
