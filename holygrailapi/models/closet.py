from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Closet(models.Model):
     title = models.CharField(max_length=20)
     # closetImage = models.CharField(nullable=True)
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=CASCADE, )
