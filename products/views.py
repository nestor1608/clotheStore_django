from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import ProductForm, CategoryForm,ValuePriceForm
from .models import ProductDataGeneral, Category,ValuesPriceProduct,SubCategory
from providers.models import Providers

from django.shortcuts import render, redirect


class ProductListView(ListView):
    model = ProductDataGeneral
    template_name = 'product/product_list.html'
    
    def get_queryset(self):
        search_term = self.request.GET.get('search', '')
        queryset = ProductDataGeneral.objects.all()
        
        if search_term:
            queryset = queryset.filter(name__icontains=search_term)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_term'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.all()
        context['providers'] = Providers.objects.all()
        context['subcategories'] = SubCategory.objects.all()
        return context



class ProductCreateView(CreateView):
    model = ProductDataGeneral
    template_name = 'product/created_product_date.html'  # Ruta a tu plantilla HTML existente
    fields = ['name', 'img', 'category', 'sub_category', 'brand', 'provider', 'number_serie', 'description']
    success_url = reverse_lazy('products:product-list')

    def form_valid(self, form):
        form.instance.user_create_price = self.request.user  # Asigna el usuario actual como creador del producto
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['price_form'] = ValuesPriceProduct()  # Crea una instancia de ValuesPriceProduct
        return context


# class CreateProductView(CreateView):
#     template_name = 'product/created_product_date.html'

#     def get(self, request):
#         product_form = ProductForm()
#         price_form =  ValuePriceForm()
#         return render(request, self.template_name, {'product_form': product_form, 'price_form': price_form})
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         context['providers'] = Providers.objects.all()
#         return context

  # Asegúrate de crear estos formularios



# class ProductCreateView(CreateView):
#     form_class = ProductoForm
#     template_name = 'product/product_form.html'
#     success_url = reverse_lazy('products:product-list')
#     model = ProductDataGeneral

#     def form_valid(self, form):
#         # Guarda el producto
#         product = form.save(commit=False)
#         product.save()

#         return super().form_valid(form)
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['categories'] = Category.objects.all()
#         context['providers'] = Providers.objects.all()
#         context['category_form'] = CategoryForm()

#         return context

class valuePriceCreateView(CreateView):
    model = ValuesPriceProduct
    form_class = ValuePriceForm
    template_name = "product/created_value-price.html"


class ProductDetailView(DetailView):
    model = ProductDataGeneral
    template_name = 'product_detail.html'
    

class ProductUpdateView(UpdateView):
    model = ProductDataGeneral
    template_name = 'product_form.html'
    fields = '__all__'
    success_url = reverse_lazy('product-list')


class ProductDeleteView(DeleteView):
    model = ProductDataGeneral
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
