from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.db import models

from django.utils.timezone import make_aware, localdate, now
from django.utils import timezone

from datetime import datetime, date, time
from collections import defaultdict
import calendar

from swipe_application.models import SwipeApplication
from attendance_application.models import AttendanceRecord
from leave_application.models import LeaveApplication


# =====================================
#  MANAGER CHECK
# =====================================
def is_manager(user):
    return user.is_staff


# =====================================
# 🔑 MANAGER LOGIN
# =====================================
def manager_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_staff:
                login(request, user)
                return redirect("manager_dashboard")
            else:
                return render(request, "manager/login.html", {
                    "error": "You are not authorized as Manager!"
                })
        else:
            return render(request, "manager/login.html", {
                "error": "Invalid username or password"
            })

    return render(request, "manager/login.html")


# =====================================
#  DASHBOARD
# =====================================
@user_passes_test(is_manager)
@login_required
def manager_dashboard(request):

    swipe_pending = SwipeApplication.objects.filter(
        manager=request.user,
        status="pending"
    )

    total_leave_requests = LeaveApplication.objects.filter(
        manager=request.user
    ).count()

    leave_pending = LeaveApplication.objects.filter(
        manager=request.user,
        status="pending"
    )

    leave_approved = LeaveApplication.objects.filter(
        manager=request.user,
        status="approved"
    )

    leave_rejected = LeaveApplication.objects.filter(
        manager=request.user,
        status="rejected"
    )

    return render(request, "manager/dashboard.html", {
        "swipe_pending": swipe_pending,
        "total_leave_requests": total_leave_requests,
        "leave_pending": leave_pending,
        "leave_approved": leave_approved,
        "leave_rejected": leave_rejected,
    })


# =====================================
#  SWIPE REQUEST
# =====================================
@user_passes_test(is_manager)
@login_required
def swipe_request(request):

    applications = SwipeApplication.objects.filter(
        manager=request.user,
        status="pending"
    )

    return render(request, "manager/swipe_request.html", {
        "applications": applications
    })


# =====================================
#  APPROVE SWIPE
# =====================================
@user_passes_test(is_manager)
@login_required
def approve_request(request, id):

    app = get_object_or_404(SwipeApplication, id=id, manager=request.user)

    app.status = "approved"
    app.save()

    user = app.user
    request_date = app.request_date

    in_datetime = make_aware(datetime.combine(request_date, app.in_time)) if app.in_time else None
    out_datetime = make_aware(datetime.combine(request_date, app.out_time)) if app.out_time else None

    filter_date = localdate(in_datetime or out_datetime)

    records = list(
        AttendanceRecord.objects.filter(
            user=user,
            timestamp__date=filter_date
        ).order_by("timestamp")
    )

    if in_datetime and out_datetime:
        if len(records) == 0:
            AttendanceRecord.objects.create(user=user, timestamp=in_datetime)
            AttendanceRecord.objects.create(user=user, timestamp=out_datetime)
        elif len(records) == 1:
            records[0].timestamp = in_datetime
            records[0].save()
            AttendanceRecord.objects.create(user=user, timestamp=out_datetime)
        else:
            records[0].timestamp = in_datetime
            records[1].timestamp = out_datetime
            records[0].save()
            records[1].save()

    elif in_datetime:
        if records:
            records[0].timestamp = in_datetime
            records[0].save()
        else:
            AttendanceRecord.objects.create(user=user, timestamp=in_datetime)

    elif out_datetime:
        if len(records) < 2:
            AttendanceRecord.objects.create(user=user, timestamp=out_datetime)
        else:
            records[1].timestamp = out_datetime
            records[1].save()

    return redirect("manager_dashboard")


# =====================================
# ❌ REJECT SWIPE
# =====================================
@user_passes_test(is_manager)
@login_required
def reject_request(request, id):

    app = get_object_or_404(SwipeApplication, id=id, manager=request.user)
    app.status = "rejected"
    app.save()

    return redirect("manager_dashboard")


# =====================================
#  LEAVE REQUEST
# =====================================
@user_passes_test(is_manager)
@login_required
def manager_leave_requests(request):

    applications = LeaveApplication.objects.filter(
        manager=request.user,
        status="pending" 
    ).order_by("-applied_at")

    return render(request, "manager/leave_request.html", {
        "applications": applications
    })

# =====================================
#  APPROVE LEAVE
# =====================================
@user_passes_test(is_manager)
@login_required
def approve_leave_request(request, id):

    leave = get_object_or_404(LeaveApplication, id=id, manager=request.user)
    leave.status = "approved"
    leave.save()

    return redirect("manager_leave_requests")


# =====================================
#  REJECT LEAVE
# =====================================
@user_passes_test(is_manager)
@login_required
def reject_leave_request(request, id):

    leave = get_object_or_404(LeaveApplication, id=id, manager=request.user)
    leave.status = "rejected"
    leave.save()

    return redirect("manager_leave_requests")


# =====================================
# 👨‍💼 EMPLOYEE LIST
# =====================================
@user_passes_test(is_manager)
@login_required
def employee_list(request):

    search = request.GET.get("search", "")

    employees = User.objects.filter(is_staff=False).order_by("username")

    if search:
        employees = employees.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search)
        )

    employee_data = []

    for emp in employees:
        employee_data.append({
            "emp": emp,
            "approved_swipe": SwipeApplication.objects.filter(user=emp, status="approved").count(),
            "rejected_swipe": SwipeApplication.objects.filter(user=emp, status="rejected").count(),
            "approved_leave": LeaveApplication.objects.filter(user=emp, status="approved").count(),
            "rejected_leave": LeaveApplication.objects.filter(user=emp, status="rejected").count(),
        })

    return render(request, "manager/employee_list.html", {
        "employees": employee_data,
        "search": search
    })


# =====================================
# 👁 VIEW EMPLOYEE ATTENDANCE
# =====================================
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from attendance_application.models import AttendanceRecord
from swipe_application.models import SwipeApplication
from leave_application.models import LeaveApplication
from collections import defaultdict
from datetime import date, datetime, time, timedelta
from django.utils import timezone
import calendar

PUBLIC_HOLIDAYS = [
    "2026-01-26",
    "2026-08-15",
    "2026-10-02",
]

@user_passes_test(is_manager)
@login_required
def view_employee_attendance(request, user_id):

    employee = get_object_or_404(User, id=user_id)

    today = timezone.now().date()
    month = int(request.GET.get("month", today.month))
    year = int(request.GET.get("year", today.year))

    # ================= ATTENDANCE =================
    records = AttendanceRecord.objects.filter(
        user=employee,
        timestamp__month=month,
        timestamp__year=year
    ).order_by('timestamp')

    grouped_records = defaultdict(list)
    for record in records:
        grouped_records[record.timestamp.date()].append(record)

    # ================= SWIPE =================
    swipes = SwipeApplication.objects.filter(
        user=employee,
        status='approved',
        request_date__month=month,
        request_date__year=year
    )

    swipe_map = {s.request_date: s for s in swipes}

    # ================= LEAVE =================
    leaves = LeaveApplication.objects.filter(
        user=employee,
        status="approved"
    )

    leave_dates = set()
    for leave in leaves:
        current = leave.from_date
        while current <= leave.to_date:
            leave_dates.add(current)
            current += timedelta(days=1)

    # ================= LOOP =================
    total_days = calendar.monthrange(year, month)[1]

    attendance_data = []
    total_minutes = 0
    total_late = 0
    total_portion = 0

    for day in range(1, total_days + 1):

        current_date = date(year, month, day)
        recs = sorted(grouped_records.get(current_date, []), key=lambda x: x.timestamp)

        swipe = swipe_map.get(current_date)

        clock_in = None
        clock_out = None
        is_swipe_in = False
        is_swipe_out = False

        # CLOCK IN
        if len(recs) >= 1:
            clock_in = recs[0]
        elif swipe and swipe.in_time:
            clock_in = swipe
            is_swipe_in = True

        # CLOCK OUT
        if len(recs) >= 2:
            clock_out = recs[1]
        elif swipe and swipe.out_time:
            clock_out = swipe
            is_swipe_out = True

        status = "DA"
        total_hours = "0h 00m"
        late_status = "--"

        # HOLIDAY
        if current_date.weekday() == 6:
            status = "WO"
        elif str(current_date) in PUBLIC_HOLIDAYS:
            status = "PH"

        # LEAVE
        if current_date in leave_dates:
            status = "LV"
            clock_in = None
            clock_out = None
            is_swipe_in = False
            is_swipe_out = False

        # LATE
        if clock_in:
            if is_swipe_in:
                check_time = clock_in.in_time
            else:
                check_time = timezone.localtime(clock_in.timestamp).time()

            if check_time > time(11, 0):
                late_status = "1"
                if not swipe:
                    total_late += 1

        # HOURS
        if clock_in and clock_out:

            if is_swipe_in:
                in_time = timezone.make_aware(datetime.combine(current_date, clock_in.in_time))
            else:
                in_time = clock_in.timestamp

            if is_swipe_out:
                out_time = timezone.make_aware(datetime.combine(current_date, clock_out.out_time))
            else:
                out_time = clock_out.timestamp

            diff = out_time - in_time
            total_seconds = int(diff.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            total_hours = f"{hours}h {minutes:02d}m"
            total_minutes += (hours * 60 + minutes)

            if status not in ["WO", "PH", "LV"]:
                if hours >= 9:
                    status = "DP"
                elif hours >= 4:
                    status = "HD"
                else:
                    status = "DA"

        # SINGLE ENTRY
        if (clock_in and not clock_out) or (clock_out and not clock_in):
            if status not in ["WO", "PH", "LV"]:
                status = "SR"

        # SWIPE FULL DAY
        if swipe and clock_in and clock_out:
            if status not in ["WO", "PH", "LV"]:
                status = "DP"

        attendance_data.append({
            "date": current_date,
            "clock_in": clock_in,
            "clock_out": clock_out,
            "status": status,
            "total_hours": total_hours,
            "late": late_status,
            "is_swipe_in": is_swipe_in,
            "is_swipe_out": is_swipe_out
        })

        total_portion += 1

    total_hours_sum = f"{total_minutes // 60}h {total_minutes % 60:02d}m"

    return render(request, "manager/view_employee_attendance.html", {
        "employee": employee,
        "records": attendance_data,
        "month": month,
        "year": year,
        "total_hours_sum": total_hours_sum,
        "total_late": total_late,
        "total_portion": total_portion,
    })

# =====================================
# 🚪 LOGOUT
# =====================================
@login_required
def manager_logout_view(request):
    logout(request)
    return redirect("manager_login")


# =====================================
# 👁 EMPLOYEE SWIPE DETAILS
# =====================================
@login_required
@user_passes_test(is_manager)
def employee_swipe_details(request, user_id):

    employee = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        swipe_id = request.POST.get("swipe_id")
        action = request.POST.get("action")

        swipe = get_object_or_404(SwipeApplication, id=swipe_id)

        if action == "approve":
            swipe.status = "approved"
        elif action == "reject":
            swipe.status = "rejected"
        elif action == "pending":
            swipe.status = "pending"

        swipe.save()

    swipe_data = SwipeApplication.objects.filter(user=employee).order_by("-request_date")

    return render(request, "manager/employee_swipe_details.html", {
        "employee": employee,
        "swipes": swipe_data,
        "approved_swipe": swipe_data.filter(status="approved").count(),
        "rejected_swipe": swipe_data.filter(status="rejected").count(),
        "pending_swipe": swipe_data.filter(status="pending").count(),
    })


# =====================================
# 👁 EMPLOYEE LEAVE DETAILS
# =====================================
@login_required
@user_passes_test(is_manager)
def employee_leave_details(request, user_id):

    employee = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        leave_id = request.POST.get("leave_id")
        action = request.POST.get("action")

        leave = get_object_or_404(LeaveApplication, id=leave_id)

        if action == "approve":
            leave.status = "approved"
        elif action == "reject":
            leave.status = "rejected"
        elif action == "pending":   # ✅ FIXED
            leave.status = "pending"

        leave.save()

    leave_data = LeaveApplication.objects.filter(user=employee).order_by("-from_date")

    return render(request, "manager/employee_leave_details.html", {
        "employee": employee,
        "leaves": leave_data,
        "approved_leave": leave_data.filter(status="approved").count(),
        "rejected_leave": leave_data.filter(status="rejected").count(),
        "pending_leave": leave_data.filter(status="pending").count(),
    })


# =====================================
#  EMPLOYEE ANALYTICS
# =====================================
def employee_analytics(request, user_id):

    employee = get_object_or_404(User, id=user_id)

    month = int(request.GET.get("month", now().month))

    swipes = SwipeApplication.objects.filter(user=employee, request_date__month=month)

    total_swipes = swipes.count()
    approved_swipes = swipes.filter(status="approved").count()
    rejected_swipes = swipes.filter(status="rejected").count()

    present_days = approved_swipes

    leaves = LeaveApplication.objects.filter(user=employee, from_date__month=month)

    total_leaves = leaves.count()
    approved_leaves = leaves.filter(status="approved").count()
    rejected_leaves = leaves.filter(status="rejected").count()

    total_days = present_days + total_leaves

    attendance_percent = (present_days / total_days * 100) if total_days > 0 else 0

    return render(request, "manager/employee_analytics.html", {
        "employee": employee,
        "month": month,
        "total_swipes": total_swipes,
        "approved_swipes": approved_swipes,
        "rejected_swipes": rejected_swipes,
        "total_leaves": total_leaves,
        "approved_leaves": approved_leaves,
        "rejected_leaves": rejected_leaves,
        "present_days": present_days,
        "total_days": total_days,
        "attendance_percent": round(attendance_percent, 2),
    })


# =====================================
# 👤 EMPLOYEE INFO
# =====================================
@login_required
@user_passes_test(is_manager)
def employee_info(request, id):

    employee = get_object_or_404(User, id=id)

    from authentication.models import UserProfile
    profile = UserProfile.objects.filter(user=employee).first()

    return render(request, "manager/employee_info.html", {
        "employee": employee,
        "profile": profile
    })

from expense_application.models import Expense

from django.db.models import Q
from expense_application.models import Expense


from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models import Q

@login_required
@user_passes_test(is_manager)
def expense_request(request):

    months = Expense.objects.filter(
        status="pending"
    ).filter(
        Q(manager=request.user) | Q(manager__isnull=True)
    ).annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Count('id')
    ).order_by('-month')

    return render(request, "manager/expense_request.html", {
        "months": months
    })

@login_required
@user_passes_test(is_manager)
def month_expenses(request, month):

    year, month = month.split('-')

    expenses = Expense.objects.filter(
        status="pending",
        date__year=year,
        date__month=month
    ).filter(
        Q(manager=request.user) | Q(manager__isnull=True)
    )

    return render(request, "manager/month_expenses.html", {
        "expenses": expenses
    })

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def bulk_action(request):

    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_expenses")
        action = request.POST.get("action")

        expenses = Expense.objects.filter(id__in=selected_ids)

        if action == "approve":
            expenses.update(status="approved")

        elif action == "reject":
            expenses.update(status="rejected")

    return redirect('manager_dashboard')  

from collections import defaultdict




@login_required
@user_passes_test(is_manager)
def employee_expenses_details(request, user_id):

    employee = get_object_or_404(User, id=user_id)

    # =========================
    # ✅ FILTER PARAMETERS
    # =========================
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    month = request.GET.get("month")  # format: YYYY-MM

    # base queryset
    expenses = Expense.objects.filter(user=employee)

    # =========================
    # ✅ DATE RANGE FILTER
    # =========================
    if start_date and end_date:
        expenses = expenses.filter(date__range=[start_date, end_date])

    # =========================
    # ✅ MONTH FILTER (YYYY-MM)
    # =========================
    if month:
        year, month_num = month.split("-")
        expenses = expenses.filter(date__year=year, date__month=month_num)

    # =========================
    # HANDLE ACTION (APPROVE/REJECT/PENDING)
    # =========================
    if request.method == "POST":
        expense_id = request.POST.get("expense_id")
        action = request.POST.get("action")

        expense = get_object_or_404(Expense, id=expense_id)

        if action == "approve":
            expense.status = "approved"
        elif action == "reject":
            expense.status = "rejected"
        elif action == "pending":
            expense.status = "pending"

        expense.save()

    # =========================
    # ORDER EXPENSES
    # =========================
    expenses = expenses.order_by("-date")

    # =========================
    # GROUP BY MONTH
    # =========================
    grouped = defaultdict(list)

    for exp in expenses:
        key = exp.date.strftime("%Y-%m")
        grouped[key].append(exp)

    data = []

    for key in sorted(grouped.keys(), reverse=True):
        items = grouped[key]
        total = sum(e.amount for e in items)

        data.append({
            "month": items[0].date,
            "expenses": items,
            "total": total
        })

    return render(request, "manager/employee_expenses_details.html", {
        "employee": employee,
        "data": data,
        "approved_expense": expenses.filter(status="approved").count(),
        "rejected_expense": expenses.filter(status="rejected").count(),
        "pending_expense": expenses.filter(status="pending").count(),
    })