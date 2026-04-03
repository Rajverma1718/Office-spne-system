from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.manager_login, name='manager_login'),
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('swipe_request/', views.swipe_request, name='swipe_request'),
    path('approve/<int:id>/', views.approve_request, name='approve_request'),
    path('reject/<int:id>/', views.reject_request, name='reject_request'),
    path('manager_logout/', views.manager_logout_view, name='manager_logout'),
]