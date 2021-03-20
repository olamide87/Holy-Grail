from holygrailapi.models.product import Product
from django.db.models.deletion import CASCADE
from django.db import models
from .closet import Closet
from .product import Product

class ClosetProduct(models.Model):
    closet_id = models.ForeignKey(Closet, on_delete=CASCADE)
    product_id = models.ForeignKey(Product,on_delete=CASCADE)
