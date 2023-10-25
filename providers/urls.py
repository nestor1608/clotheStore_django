from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'providers'

urlpatterns = [
    path('created_provider/', login_required(views.ProviderCreateView.as_view()), name='provider_create'),
    path('listar/', login_required(views.ProviderListView.as_view()), name='provider_list'),
]
