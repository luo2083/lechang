from django.db import models


# Create your models here.
class Images(models.Model):
    url = models.URLField(max_length=200, default='')