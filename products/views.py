from .forms import ProductoForm, CategoryForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .models import Product, Category
from providers.models import Providers
from django.views.decorators.csrf import csrf_exempt


class ProductListView(ListView):
    model = Product
    template_name = 'product/product_list.html'
    
    def get_queryset(self):
        search_term = self.request.GET.get('search', '')
        queryset = Product.objects.all()
        
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.all()
        context['providers'] = Providers.objects.all()
        return context

class AutocompleteProductsView(TemplateView):
    def get(self, request, *args, **kwargs):
        term = request.GET.get('term', '')
        products = Product.objects.filter(name__icontains=term).values()[:10]  # Limita a 10 sugerencias
        results = [{'id':product['id'],'text':product['name']} for product in products]
        return JsonResponse(results, safe=False)
    
class ProductSearchView(TemplateView):
    def get(self, request, *args, **kwargs):
        search_term = request.GET.get('search_term', '')
        products = Product.objects.filter(name__icontains=search_term)
        data = [{'id': product.id, 'name': product.name} for product in products]
        return JsonResponse({'results': data})



class ProductCreateView(CreateView):
    form_class = ProductoForm
    template_name = 'product/product_form.html'
    success_url = reverse_lazy('products:product-list')
    model = Product

    def form_valid(self, form):
        # Guarda el producto
        product = form.save(commit=False)
        product.save()

        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['providers'] = Providers.objects.all()
        context['category_form'] = CategoryForm()

        return context



class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'product_form.html'
    fields = '__all__'
    success_url = reverse_lazy('product-list')


class ProductDeleteView(DeleteView):
    model = Product
    template_name = None
    success_url = reverse_lazy('product-list')



class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'


class CategoryCreateView(CreateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = '__all__'
    
    def post(self, request, *args, **kwargs):
        category_form = self.get_form()
        
        if category_form.is_valid():
            try:
                category = category_form.save()  # Intenta guardar la categoría
                return JsonResponse({'success': True, 'message': 'Categoría creada con éxito'})
            except Exception as e:
                response_data = {
                    'success': False,
                    'error_message': str(e)
                }
                return JsonResponse(response_data, status=500)
        else:
            # Formulario no válido, devuelve detalles de los errores
            errors = category_form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categoria_detail.html'

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = '__all__'
    success_url = reverse_lazy('products:product-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.object.name  # Agrega el nombre al contexto
        return context




class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('products:category-list')  # La URL a la que redireccionar después de la eliminación

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response_data = {'message': 'El objeto ha sido eliminado exitosamente.'}
        return JsonResponse(response_data)
