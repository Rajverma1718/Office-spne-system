from django.urls import path
from . import views

urlpatterns = [

    # =====================================
    # 🔐 AUTH
    # =====================================
    path('login/', views.manager_login, name='manager_login'),
    path('logout/', views.manager_logout_view, name='manager_logout'),

    # =====================================
    # 🏠 DASHBOARD
    # =====================================
    path('dashboard/', views.manager_dashboard, name='manager_dashboard'),

    # =====================================
    # 📥 SWIPE REQUESTS
    # =====================================
    path('swipe-request/', views.swipe_request, name='swipe_request'),
    path('swipe-approve/<int:id>/', views.approve_request, name='approve_request'),
    path('swipe-reject/<int:id>/', views.reject_request, name='reject_request'),

    # =====================================
    # 📝 LEAVE REQUESTS
    # =====================================
    path('leave-requests/', views.manager_leave_requests, name='manager_leave_requests'),
    path('leave-approve/<int:id>/', views.approve_leave_request, name='approve_leave_request'),
    path('leave-reject/<int:id>/', views.reject_leave_request, name='reject_leave_request'),

    # =====================================
    # 👥 EMPLOYEES
    # =====================================
    path('employees/', views.employee_list, name='employee_list'),
    path('employee/<int:user_id>/attendance/', views.view_employee_attendance, name='view_employee_attendance'),
    path('employee/<int:user_id>/swipes/', views.employee_swipe_details, name='employee_swipe_details'),
    path('employee/<int:user_id>/leaves/', views.employee_leave_details, name='employee_leave_details'),
    path('employee/<int:user_id>/analytics/', views.employee_analytics, name='employee_analytics'),
    path('employee/<int:id>/', views.employee_info, name='employee_info'),

    # =====================================
    # 💰 EXPENSE SYSTEM (CLEAN STRUCTURE)
    # =====================================

    # Main expense page (month wise)
    path('expenses/', views.expense_request, name='expense_request'),

    # Month filter page
    path('expenses/month/<str:month>/', views.month_expenses, name='month_expenses'),

    # Bulk actions
    path('expenses/bulk-action/', views.bulk_action, name='bulk_action'),

    # Employee expenses
    path('employee/<int:user_id>/expenses/', views.employee_expenses_details, name='employee_expenses_details'),
]