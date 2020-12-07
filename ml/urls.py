from django.urls import path
from . import views
urlpatterns = [
    path('get_sts', views.get_sts),
    path('get_ml', views.UrlView.as_view()),
]