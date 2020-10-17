from django.urls import path
from . import views

urlpatterns = [
    path('', views.SearchView, name='search'),
    path(r'shops$', views.ShopsView, name='shops'),
    path(r'how_to_use$', views.HowToUseView, name='how_to_use'),
    path('<path>/mypage/', views.MypageView, name = 'mypage'),
    path(r'history', views.HistoryView, name='history'),
    # path('password_change/', views.PasswordChange.as_view(), name='password_change'), 
    # path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    
]