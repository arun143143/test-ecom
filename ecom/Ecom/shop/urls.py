from django.urls import path
from . import views

urlpatterns = [
    # Home and Products
    path('', views.home, name='home'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('category/<int:id>/', views.category_view, name='category'),
    
    # Product CRUD
    path('products/', views.product_list, name='product_list'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/<int:id>/update/', views.product_update, name='product_update'),
    path('product/<int:id>/delete/', views.product_delete, name='product_delete'),
    
    # Category CRUD
    path('categories/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/<int:id>/update/', views.category_update, name='category_update'),
    path('category/<int:id>/delete/', views.category_delete, name='category_delete'),
    
    # User CRUD
    path('users/', views.user_list, name='user_list'),
    path('user/<int:id>/', views.user_detail, name='user_detail'),
    path('user/create/', views.user_create, name='user_create'),
    path('user/<int:id>/update/', views.user_update, name='user_update'),
    path('user/<int:id>/delete/', views.user_delete, name='user_delete'),
    
    # Cart
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove-from-cart/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Checkout and Orders
    path('checkout/', views.checkout, name='checkout'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('my-orders/', views.my_orders, name='my_orders'),
    
    # Order Management
    path('orders/', views.order_list, name='order_list'),
    path('order/<int:id>/', views.order_detail, name='order_detail'),
    path('order/<int:id>/update/', views.order_update_status, name='order_update'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
