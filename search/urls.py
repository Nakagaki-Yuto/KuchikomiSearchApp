from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchView, name='search'),
    path('shops/', views.ShopsView, name='shops'),
    path('how_to_use/', views.HowToUseView, name='how_to_use'),
    path('mypage/', views.MypageView, name='mypage'),
    path('favorite/<str:shop_id>/', views.FavoriteView, name='favorite'),
    path('favorite_shops/', views.FavoriteShopsView, name='favorite_shops'),
    path('password_change/', views.PasswordChange.as_view(), name='password_change'), 
    path('password_change/done/', views.PasswordChangeDoneView, name='password_change_done'),
]