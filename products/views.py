from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import ProductForm, CategoryForm, ValuesPriceProductForm
from .models import ProductDataGeneral, Category,ValuesPriceProduct,Article, ProductCost, ItemProductCost,ModelClothing
from providers.models import Providers
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

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
        context['subcategories'] = Article.objects.all()
        return context

class CreateCardProductView(TemplateView):
    template_name = "product/card_create_product.html"


class CreateProductView(CreateView):
    model = ProductDataGeneral
    template_name = 'product/created_product_date.html'
    fields = [ 'article', 'brand','color','description','img', 'provider', 'number_serie', ]
    success_url = reverse_lazy('products:product-card')  # Reemplaza con la URL adecuada

    def form_valid(self, form):
        form.instance.user_create_price = self.request.user  # Asigna el usuario actual como creador del producto
        response = super().form_valid(form)
        product_id = self.object.id  # Obtiene el ID del producto creado
        return JsonResponse({'id': product_id})  


class ValuePriceCreateView(CreateView):
    model = ValuesPriceProduct
    fields = '__all__'
    template_name = "product/price/created_value_price.html"

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        id_product = self.kwargs.get('id_product')
        form_kwargs = {'id_product': id_product}
        form = ValuesPriceProductForm(**form_kwargs)  # Utiliza el constructor del formulario
        return form



class CategoryCreateView(CreateView):
    model = Category
    template_name = 'product/category/create_category.html'
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
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all() 
        return context


class ArticleCreateView(CreateView):
    model = Article
    template_name = 'product/article/create_article.html'
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        article_form = self.get_form()
        
        if article_form.is_valid():
            try:
                article = article_form.save()  # Intenta guardar la categoría
                return JsonResponse({'success': True, 'message': 'Categoría creada con éxito'})
            except Exception as e:
                response_data = {
                    'success': False,
                    'error_message': str(e)
                }
                return JsonResponse(response_data, status=500)
        else:
            # Formulario no válido, devuelve detalles de los errores
            errors = article_form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category_list"] = Category.objects.all() 
        context["article_list"] = Article.objects.all() 
        return context
    
    
class ClothingModelCreateView(CreateView):
    model = Article
    template_name = 'product/clothing_model/create_clothing_model.html'
    fields = '__all__'
    
    def post(self, request, *args, **kwargs):
        clothing_model_form = self.get_form()
        
        if clothing_model_form.is_valid():
            try:
                clothing_model = clothing_model_form.save()  # Intenta guardar la categoría
                return JsonResponse({'success': True, 'message': 'Categoría creada con éxito'})
            except Exception as e:
                response_data = {
                    'success': False,
                    'error_message': str(e)
                }
                return JsonResponse(response_data, status=500)
        else:
            # Formulario no válido, devuelve detalles de los errores
            errors = clothing_model_form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article_list'] = Article.objects.all()
        context["clothing_model_list"] = ModelClothing.objects.all() 
        return context





class CategoryList(ListView):
    model = Category
    context_object_name = 'category_list'
    
    
    
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



class ProductCostCreateView(CreateView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        product_cost = ProductCost.objects.create(amount=0)
        return JsonResponse({'id_product': product_cost.id})

class ItemProductCostCreateView(CreateView):
    model = ItemProductCost
    template_name = 'itemproductcost_form.html'
    fields = ['description_cost', 'amounts_cost', 'add_price']

    def get_initial(self):
        # Obtiene el id del ProductCost pasado en la URL
        id_product_cost = self.kwargs['id_product_cost']
        return {'id_product_cost': id_product_cost}
    
    def form_valid(self, form):
        # Obtén el ProductCost relacionado con este ItemProductCost
        id_product_cost = self.kwargs['id_product_cost']
        product_cost = ProductCost.objects.get(id=id_product_cost)

        # Crea una nueva instancia de ItemProductCost
        item_cost = form.save(commit=False)
        item_cost.id_product_cost = product_cost
        item_cost.save()

        # Actualiza el campo 'amount' del ProductCost sumando todos los amounts de los ItemProductCost relacionados
        product_cost.amount = product_cost.itemproductcost_set.aggregate(total_amount=sum('amounts_cost'))['total_amount'] or 0
        product_cost.save()

        return super().form_valid(form)

# class ProductCostListView(ListView):
#     model = ProductCost
#     template_name = 'productcost_list.html'
#     context_object_name = 'product_costs'

# class ItemProductCostListView(ListView):
#     model = ItemProductCost
#     template_name = 'itemproductcost_list.html'
#     context_object_name = 'item_costs'
