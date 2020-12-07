from django.urls import path
from . import views

urlpatterns = [
    path('user', views.UserView.as_view()),
    path('authorize',views.authorize),
    path('status', views.get_staus, name='status'),
    path('logout', views.logout, name='logout')
]
