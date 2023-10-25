
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Providers




class ProviderCreateView(CreateView):
    model = Providers
    template_name = 'product_image_create.html'
    fields = '__all__'
    success_url = reverse_lazy('product-list')



class ProviderListView(ListView):
    model = Providers
    template_name = 'providers/proveedor_list.html'

