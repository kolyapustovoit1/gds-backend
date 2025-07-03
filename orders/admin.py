from django.contrib import admin
from .models import Order

# Реєструємо модель Order в адмін-панелі
admin.site.register(Order)