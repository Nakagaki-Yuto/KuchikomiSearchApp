from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_screen, name='search_screen'),
]