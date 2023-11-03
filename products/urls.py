from django.urls import path
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'products'

urlpatterns = [
    path('product_list/', login_required(views.ProductListView.as_view()), name='product-list'),
    
    path('product_card/', login_required(views.CreateCardProductView.as_view()), name='product-card'),
    
    path('product_detail/<int:pk>/', login_required( views.ProductDetailView.as_view()), name='product-detail'),
    path('product_updated/<int:pk>/editar/', login_required( views.ProductUpdateView.as_view()), name='product-update'),
    path('product_deleted/<int:pk>/eliminar/',login_required( views.ProductDeleteView.as_view()), name='product-delete'),
    
    # path('products/autocomplete/', login_required(views.AutocompleteProductsView.as_view()), name='autocomplete-products'),

    path('category_list/', login_required(views.CategoryList.as_view()), name='category-list'),
    
    path('product_add/', login_required( views.CreateProductView.as_view()), name='product-create'),
    path('productcost_add/', views.ProductCostCreateView.as_view(), name='productcost_create'),
    path('product_value_price_add/',login_required(views.ValuePriceCreateView.as_view()), name='value-price-create'),
    
    path('product_value_price_add/<int:product_id>/',login_required(views.ValuePriceCreateView.as_view()), name='value-price'),
    
    path('category_add/', login_required(views.CategoryCreateView.as_view()), name='category-create'),
    path('article_add/', login_required(views.ArticleCreateView.as_view()), name='article-create'),
    path('clothing_model_add/', login_required(views.ClothingModelCreateView.as_view()), name='clothing-model-create'),
    path('color_add/', login_required(views.ColorCreateView.as_view()), name='color-create'),
    path('brand_add/', login_required(views.BrandCreateView.as_view()), name='brand-create'),
    
    
    path('category_detail/<int:pk>/', login_required( views.CategoryDetailView.as_view()), name='category-detail'),
    path('category_updated/<int:pk>/edit/',login_required( views.CategoryUpdateView.as_view()), name='category-update'),
    path('category_deleted/<int:pk>/delete/', login_required(views.CategoryDeleteView.as_view()), name='category-delete'),
    
    path('create_item_cost/<int:id_product_cost>/', views.ItemProductCostCreateView.as_view(), name='create_item_cost'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)