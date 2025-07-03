from rest_framework import serializers
from .models import Order # <-- Імпорт тепер локальний

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'article', 'product_name', 'created_at', 'file']