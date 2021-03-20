from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from .closet import Closet

class Product(models.Model):
     product_name = models.CharField(max_length=50)
     color = models.CharField(max_length=50)
     image = models.ImageField(upload_to='items', height_field=None, width_field=None, max_length=None, null=True)
     price = models.FloatField(validators=[MinValueValidator(0.00), MaxValueValidator(200000.00)],)
     owns = models.BooleanField(default=True)



