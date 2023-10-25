from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'products'

urlpatterns = [
    path('product_list/', login_required(views.ProductListView.as_view()), name='product-list'),
    path('product_add/add/', login_required( views.ProductCreateView.as_view()), name='product-create'),
    path('product_detail/<int:pk>/', login_required( views.ProductDetailView.as_view()), name='product-detail'),
    path('product_updated/<int:pk>/editar/', login_required( views.ProductUpdateView.as_view()), name='product-update'),
    path('product_deleted/<int:pk>/eliminar/',login_required( views.ProductDeleteView.as_view()), name='product-delete'),
    path('products/autocomplete/', login_required(views.AutocompleteProductsView.as_view()), name='autocomplete-products'),

    path('category_list/',login_required( views.CategoryListView.as_view()), name='category-list'),
    path('category_add/add/', login_required(views.CategoryCreateView.as_view()), name='category-create'),
    path('category_detail/<int:pk>/', login_required( views.CategoryDetailView.as_view()), name='category-detail'),
    path('category_updated/<int:pk>/edit/',login_required( views.CategoryUpdateView.as_view()), name='category-update'),
    path('category_deleted/<int:pk>/delete/', login_required(views.CategoryDeleteView.as_view()), name='category-delete'),
]
