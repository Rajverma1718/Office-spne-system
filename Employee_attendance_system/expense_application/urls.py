from django.urls import path
from . import views

urlpatterns = [
    path('expense_home/', views.expense_home, name='expense_home'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('add_voucher/', views.add_voucher, name='add_voucher'),
]