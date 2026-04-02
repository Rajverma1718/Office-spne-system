from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='user_login'),
    path('home', views.home, name='home'),
    path('id_card', views.id_card, name='id_card'),
    path('profile', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),
]