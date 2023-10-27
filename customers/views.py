from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, UpdateView,DetailView,ListView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .models import Customer, Address
from .forms import CustomerAddressForm

class ClienteCreateView(CreateView):
    model = Customer
    form_class = CustomerAddressForm
    template_name = 'crear_cliente.html'
    success_url = reverse_lazy('cliente_list')

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