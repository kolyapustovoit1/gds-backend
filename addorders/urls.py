from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.add_order, name='add-order'),
]