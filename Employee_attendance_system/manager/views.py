from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from swipe_application.models import SwipeApplication
from attendance_application.models import AttendanceRecord
from django.utils import timezone
from datetime import datetime


def manager_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('manager_dashboard')
            else:
                return render(request, 'manager/login.html', {
                    'error': 'You are not authorized as Manager!'
                })
        else:
            return render(request, 'manager/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'manager/login.html')


@login_required
def manager_dashboard(request):
    if not request.user.is_staff:
        return redirect('user_login')

    applications = SwipeApplication.objects.filter(
        manager=request.user,
        status='pending'
    )

    return render(request, 'manager/dashboard.html', {
        'applications': applications
    })


@login_required
def swipe_request(request):
    if not request.user.is_staff:
        return redirect('user_login')

    applications = SwipeApplication.objects.filter(
        manager=request.user,
        status='pending'
    )

    return render(request, 'manager/swipe_request.html', {
        'applications': applications
    })


# ✅🔥 FINAL APPROVE LOGIC (ATTENDANCE UPDATE)
@login_required
def approve_request(request, id):

    app = SwipeApplication.objects.get(id=id, manager=request.user)

    # ✅ Approve request
    app.status = 'approved'
    app.save()

    user = app.user
    request_date = app.request_date

    # ✅ Convert to datetime
    in_datetime = None
    out_datetime = None

    if app.in_time:
        in_datetime = timezone.make_aware(
            datetime.combine(request_date, app.in_time)
        )

    if app.out_time:
        out_datetime = timezone.make_aware(
            datetime.combine(request_date, app.out_time)
        )

    # ✅ Get existing attendance records
    records = AttendanceRecord.objects.filter(
        user=user,
        timestamp__date=request_date
    ).order_by('timestamp')

    # 🔹 IN TIME UPDATE
    if in_datetime:
        if records.exists():
            first_record = records.first()
            first_record.timestamp = in_datetime
            first_record.save()
        else:
            AttendanceRecord.objects.create(
                user=user,
                timestamp=in_datetime
            )

    # 🔹 OUT TIME UPDATE
    if out_datetime:
        if records.count() >= 2:
            second_record = records[1]
            second_record.timestamp = out_datetime
            second_record.save()
        else:
            AttendanceRecord.objects.create(
                user=user,
                timestamp=out_datetime
            )

    return redirect('manager_dashboard')


@login_required
def reject_request(request, id):
    app = SwipeApplication.objects.get(id=id, manager=request.user)
    app.status = 'rejected'
    app.save()
    return redirect('manager_dashboard')

@login_required
def manager_logout_view(request):
    logout(request)
    return redirect('manager_login')