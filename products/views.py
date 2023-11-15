from django.http import JsonResponse
from django.urls import reverse_lazy,reverse
from decimal import Decimal
from django.db.models import Sum
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, TemplateView
from .forms import ItemProductCostForm, ValuesPriceProductForm
from .models import ProductDataGeneral, Category,ValuesPriceProduct,Article, ProductCost, ItemProductCost,ModelClothing, Brand, ColorModel
from providers.models import Providers
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

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


# -------------------------------------- create ------------------------------------
class CreateCardProductView(TemplateView):
    template_name = "product/card_create_product.html"


class CreateProductView(CreateView):
    model = ProductDataGeneral
    template_name = 'product/created_product_date.html'
    fields = [ 'article', 'brand','gener','color','description','img', 'provider', 'number_serie', ]


    def form_valid(self, form):
        form.instance.user_create_price = self.request.user  
        return super().form_valid(form)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        return JsonResponse({'message':f'algo salio mal{form.errors}'})
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['choices_gener'] = ProductDataGeneral.CHOICE_GENERE
        return context
    
    def get_success_url(self):
        product_id = self.object.id
        return reverse_lazy('products:value-price', kwargs={'product_id': product_id})


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
    model = ModelClothing
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


class ProductCostCreateView(CreateView):
    @method_decorator(csrf_exempt)
    def post(self, request):
        product_cost = ProductCost.objects.create(amount_total_percentage=0)
        return JsonResponse({'id_product': product_cost.id})


class ItemProductCostCreateView(CreateView):
    model = ItemProductCost
    template_name = 'product/cost/create_item_cost.html'
    form_class = ItemProductCostForm
    success_url = reverse_lazy('products:dashboard_card')

    def get_initial(self):
        # Obtiene el id del ProductCost pasado en la URL
        id_product_cost = self.kwargs['id_product_cost']
        return {'id_product_cost': id_product_cost,'id_product': self.kwargs.get('id_product', None)}
    
    
    def get_product_id(self,):
        product_cost = ProductCost.objects.get(id=self.kwargs['id_product_cost'])
        return product_cost.id_product


    def form_valid(self, form):
        # Obtén el ProductCost relacionado con este ItemProductCost
        id_product_cost = self.kwargs['id_product_cost']
        product_cost = ProductCost.objects.get(id=id_product_cost)


        # Crea una nueva instancia de ItemProductCost
        item_cost = form.save(commit=False)
        item_cost.id_product_cost = product_cost
        item_cost.save()

        
        # Actualiza el campo 'amount' del ProductCost sumando todos los amounts de los ItemProductCost relacionados
        total_amount = product_cost.itemproductcost_set.aggregate(total_amount=Sum('amounts_cost'))['total_amount'] or 0
        # Obtener el id_product desde la URL o desde el formulario
        print("Formulario válido")
        # Obtener el id_product desde el URL o desde el formulario
        id_product = self.kwargs.get('id_product') or form.cleaned_data.get('id_product', None)

        # Obtener la instancia de ProductDataGeneral
        product_data_general = ProductDataGeneral.objects.get(id=id_product)

        # Asignar la instancia a id_product de ProductCost
        product_cost.id_product = product_data_general
        product_cost.save()
        # print(id_product)
        # print("Datos del formulario:", form.cleaned_data)
        product_cost.id_product_id = id_product
        product_cost.amount_total_percentage = Decimal(total_amount)
        product_cost.save()
        
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_product_id()
        context['product_list'] = ProductDataGeneral.objects.all() 
        return context
    


class BrandCreateView(CreateView):
    model = Brand
    fields = '__all__'
    template_name = "product/brand/create_brand.html"
    
    def form_valid(self, form):
        form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["brand_list"] = Brand.objects.all()
        return context


class ColorCreateView(CreateView):
    model = ColorModel
    fields = '__all__'
    template_name = "product/color/create_color.html"
    
    def form_valid(self, form):
        # Customize the behavior when the form is valid
        # For example, you can save the form and return a JSON response
        form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, form):
        # Customize the behavior when the form is invalid
        # For example, return a JSON response with errors
        errors = form.errors.as_json()
        return JsonResponse({'success': False, 'errors': errors})
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["color_list"] = ColorModel.objects.all()
        return context


#------------------------------------- UPDATE--------------------------------------


class ProductUpdateView(UpdateView):
    model = ProductDataGeneral
    template_name = 'product_form.html'
    fields = '__all__'
    success_url = reverse_lazy('product-list')


class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category/category_form.html'
    fields = '__all__'
    success_url = reverse_lazy('products:product-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.object.name  # Agrega el nombre al contexto
        return context


class ArticleUpdateView(UpdateView):
    model = Article
    template_name = "product/article/create_article.html"


class ClothingModelUpdateView(UpdateView):
    model = ModelClothing
    template_name = "product/clothing_model/create_clothing_model.html"


class ProductCostUpdateView(UpdateView):
    model = ProductCost
    template_name = ".html"


class ItemProductCostUpdateView(UpdateView):
    model = ItemProductCost
    template_name = ".html"


class BrandUpdateView(UpdateView):
    model = Brand
    template_name = ".html"


class ColorUpdateView(UpdateView):
    model = ColorModel
    template_name = ".html"



# ------------------------------------------------------ DELETE -----------------------------------------

class ProductDeleteView(DeleteView):
    model = ProductDataGeneral
    template_name = None
    success_url = reverse_lazy('product-list')


class ProductDetailView(DetailView):
    model = ProductDataGeneral
    template_name = 'product_detail.html'
    

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'categoria_detail.html'





class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('products:category-list')  # La URL a la que redireccionar después de la eliminación

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        response_data = {'message': 'El objeto ha sido eliminado exitosamente.'}
        return JsonResponse(response_data)

