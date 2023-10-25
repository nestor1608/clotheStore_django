from decimal import Decimal

from .models import Product

class CarritoCompra:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get('carrito')
        if not carrito:
            carrito = self.session['carrito'] = {}
        self.carrito = carrito

    def agregar(self, producto_id, cantidad):
        producto_id = str(producto_id)
        if producto_id not in self.carrito:
            self.carrito[producto_id] = {'cantidad': 0, 'precio': str(Product.objects.get(id=producto_id).precio)}

        self.carrito[producto_id]['cantidad'] += cantidad
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session['carrito'] = self.carrito
        self.session.modified = True

    def eliminar(self, producto_id):
        producto_id = str(producto_id)
        if producto_id in self.carrito:
            del self.carrito[producto_id]
            self.guardar_carrito()

    def __iter__(self):
        productos = Product.objects.filter(id__in=self.carrito.keys())
        carrito = self.carrito.copy()
        for producto in productos:
            carrito[str(producto.id)]['producto'] = producto

        for item in carrito.values():
            item['precio'] = Decimal(item['precio'])
            item['precio_total'] = item['precio'] * item['cantidad']
            yield item

    def __len__(self):
        return sum(item['cantidad'] for item in self.carrito.values())

    def obtener_precio_total(self):
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.carrito.values())

    def limpiar_carrito(self):
        del self.session['carrito']
        self.session.modified = True


# venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
#     producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
#     cantidad = models.PositiveIntegerField(default=1)
#     precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
#     importe_total = models.DecimalField(max_digits=10, decimal_places=2)