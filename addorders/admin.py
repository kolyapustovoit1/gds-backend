from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'product_name', 'created_at', 'file')
    search_fields = ('article', 'product_name')
    list_filter = ('created_at',)