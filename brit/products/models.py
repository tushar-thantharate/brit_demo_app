from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Products(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="user", null=True, blank=True
    )
    name = models.CharField(max_length=1024, verbose_name="product_name")
    price = models.IntegerField(verbose_name="product_price")
