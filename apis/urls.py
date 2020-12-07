from django.urls import path
from .views import weather, menu

urlpatterns = [
    path('weather', weather.WeatherView.as_view()),
    path('menu', menu.get_menu),
]