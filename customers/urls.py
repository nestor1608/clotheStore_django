from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (
    CreateCustomerAddressView, CreateAddressView,
    CustomerDetailView, AddressDetailView,
    CustomerUpdateView, AddressUpdateView,
    CustomerListView, AddressListView
)

app_name = 'customers'  

urlpatterns = [
    path('customer/create/', login_required(CreateCustomerAddressView.as_view()), name='create_customer'),
    path('customer/<int:pk>/', login_required(CustomerDetailView.as_view()), name='customer_detail'),
    path('customer/update/<int:pk>/', login_required(CustomerUpdateView.as_view()), name='customer_update'),
    path('customer/list/', login_required(CustomerListView.as_view()), name='customer_list'),
    
    path('address/create/', login_required(CreateAddressView.as_view()), name='create_address'),
    path('address/<int:pk>/', login_required(AddressDetailView.as_view()), name='address_detail'),
    path('address/update/<int:pk>/', login_required(AddressUpdateView.as_view()), name='address_update'),
    path('address/list/', login_required(AddressListView.as_view()), name='address_list'),
]
