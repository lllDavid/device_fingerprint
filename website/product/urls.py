from django.urls import path
from .views import add_to_cart
from . import views

urlpatterns = [
    path('', views.ProductGridView.as_view(), name='product-grid'),  
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove-from-cart'),  
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product-detail'), 
    path('products', views.search_products, name='search-products'),
]
