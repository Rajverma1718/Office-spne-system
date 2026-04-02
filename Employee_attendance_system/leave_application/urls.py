from django.urls import path
from . import views

urlpatterns = [
    path('leave_home/', views.leave_home, name='leave_home'),
    path('leave_apply/', views.leave_apply, name='leave_apply'),
    path('recent_leave/', views.recent_leave, name='recent_leave'),
    path('approve_leave/', views.approve_leave, name='approve_leave'),
    path('reject_leave/', views.reject_leave, name='reject_leave'),
    path('lapsed_leave/', views.lapsed_leave, name='lapsed_leave'),
    
]