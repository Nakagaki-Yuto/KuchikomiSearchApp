from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('shops', views.shops, name='shops'),
    path('how_to_use', views.how_to_use, name='how_to_use'),
    
]