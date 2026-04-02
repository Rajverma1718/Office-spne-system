from django.urls import path
from . import views

urlpatterns = [
    path('swipe_home/', views.swipe_home, name='swipe_home'),
    path('swipe_apply/', views.swipe_apply, name='swipe_apply'),
    path('recent_swipe/', views.recent_swipe, name='recent_swipe'),
    path('approve_swipe/', views.approve_swipe, name='approve_swipe'),
    path('reject_swipe/', views.reject_swipe, name='reject_swipe'),
    # path('lapsed_swipe/', views.lapsed_swipe, name='lapsed_swipe'),
]