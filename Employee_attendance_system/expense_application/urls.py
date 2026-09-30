from django.urls import path
from . import views

urlpatterns = [

    # HOME
    path('', views.expense_home, name='expense_home'),

    # ADD EXPENSE
    path('add-expense/', views.add_expense, name='add_expense'),

    # RECENT EXPENSES (PENDING)
    path('recent-expenses/', views.recent_expenses, name='recent_expenses'),

    # ✅ APPROVED EXPENSES (ADD)
    path('approved-expenses/', views.approve_expenses, name='approve_expenses'),

    # ❌ REJECTED EXPENSES (ADD)
    path('rejected-expenses/', views.reject_expenses, name='reject_expenses'),

    # ADD VOUCHER (SEARCH + RESULT PAGE)
    path('add-voucher/', views.add_voucher, name='add_voucher'),

    # MONTHLY DETAIL
    path('monthly/<int:year>/<int:month>/<str:status>/', views.monthly_detail, name='monthly_detail'),

]