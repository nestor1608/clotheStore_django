from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name ='sales'

urlpatterns = [
    path('sales/',login_required(views.SaleView.as_view()), name='created_sales'),
]
