from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

class Closet(models.Model):
     title = models.CharField(max_length=20)
     user_id = models.ForeignKey("HolygrailUser", on_delete=CASCADE, related_name="holygrailuser")
