from django.db import models

class Order(models.Model):
    article = models.CharField(max_length=255)
    product_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='order_excels/')

    def __str__(self):
        return f"Order {self.id} - {self.product_name}"
