from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('orders/', views.all_orders, name='orders'),
    path('orders/delete/<int:order_id>/', views.delete_order, name='delete_order'),
    path('distribution/<int:order_id>/', views.distribute_order, name='distribution'),
]