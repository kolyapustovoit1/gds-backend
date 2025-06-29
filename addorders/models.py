from django.db import models
from django.utils import timezone

import uuid
from django.db import models
from django.utils import timezone


class Order(models.Model):
    article = models.CharField(max_length=50)
    product_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    file = models.FileField(upload_to='order_excels/')

    def __str__(self):
        return f"{self.product_name} ({self.article})"