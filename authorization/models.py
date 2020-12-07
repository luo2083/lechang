from django.db import models
from ml.models import Images
from apis.models import App

class User(models.Model):
    open_id = models.CharField(max_length=32, unique=True)
    nicknaame = models.CharField(max_length=256)
    focus_cropId = models.TextField(default='[]')
    focus_city = models.TextField(default='[]')
    image = models.ManyToManyField(Images)
    menu = models.ManyToManyField(App)