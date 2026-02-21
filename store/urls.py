from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('register/', views.register, name='register'),
    path('redirect-after-login/', views.redirect_after_login, name='redirect_after_login'),
path('dashboard/products/', views.admin_product_list, name='admin_product_list'),
path('dashboard/products/add/', views.admin_product_create, name='admin_product_create'),
path('dashboard/products/edit/<int:pk>/', views.admin_product_update, name='admin_product_update'),
path('dashboard/products/delete/<int:pk>/', views.admin_product_delete, name='admin_product_delete'),
]