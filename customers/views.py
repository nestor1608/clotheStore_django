from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView,DetailView,ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Customer, Address
from .forms import CustomerAddressForm

class CreateCustomerAddressView(CreateView):
    template_name = 'template.html'
    form_class = CustomerAddressForm
    success_url = reverse_lazy('customers:customer_detail')  # Reemplaza 'nombre_de_la_vista_de_exito'

    def form_valid(self, form):
        # Guardar el formulario sin commit para obtener el cliente
        customer = form.save(commit=False)
        customer.save()

        # Obtener la instancia de Address del formulario
        address = form.cleaned_data.get('address')  # Asegúrate de que este sea el nombre correcto del campo en tu formulario

        if address:
            # Establecer el campo id_cliente de Address con el ID del cliente
            address.id_cliente = customer.customer_id
            address.save()

        return super().form_valid(form)

class CustomerDetailView(DetailView):
    model = Customer
    template_name = 'customer_detail.html'
    context_object_name = 'customer'

class CreateAddressView(CreateView):
    model = Address
    form_class = CustomerAddressForm
    template_name = 'address_form.html'
    success_url = reverse_lazy('customers:address_detail')  

class AddressDetailView(DetailView):
    model = Address
    template_name = 'address_detail.html'
    context_object_name = 'address'

class CustomerUpdateView(UpdateView):
    model = Customer
    form_class = CustomerAddressForm
    template_name = 'customer_form.html'  
    success_url = reverse_lazy('customers:customer_list')  

class CustomerListView(ListView):
    model = Customer
    template_name = 'customer_list.html'
    context_object_name = 'customers'


class AddressUpdateView(UpdateView):
    model = Address
    form_class = CustomerAddressForm
    template_name = 'address_form.html'  
    success_url = reverse_lazy('customers:address_list')  

class AddressListView(ListView):
    model = Address
    template_name = 'address_list.html'
    context_object_name = 'addresses'