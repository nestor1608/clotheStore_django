from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from .models import Cliente, Empleado
from .forms import ClienteForm, EmpleadoForm

class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'crear_cliente.html'
    success_url = reverse_lazy('cliente_list')

class EmpleadoCreateView(CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'crear_empleado.html'
    success_url = reverse_lazy('empleado_list')

class EmpleadoListView(ListView):
    model = Empleado
    template_name = 'lista_empleados.html'

class EmpleadoUpdateView(UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'editar_empleado.html'
    success_url = reverse_lazy('empleado_list')

class EmpleadoDeleteView(DeleteView):
    model = Empleado
    template_name = 'eliminar_empleado.html'
    success_url = reverse_lazy('empleado_list')
