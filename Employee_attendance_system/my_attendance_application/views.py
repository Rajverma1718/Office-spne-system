from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from attendance_application.models import AttendanceRecord
from collections import defaultdict
from datetime import time
from django.utils import timezone


# Public Holiday List
PUBLIC_HOLIDAYS = [
    "2026-01-26",
    "2026-08-15",
    "2026-10-02",
]


@login_required
def my_attendance_home(request):

    today = timezone.now().date()
    current_month = today.month
    current_year = today.year

    archive = request.GET.get("archive")

    records = AttendanceRecord.objects.filter(
        user=request.user
    ).order_by('timestamp')

    # Archive tick → previous months
    if archive == "on":
        records = records.exclude(
            timestamp__month=current_month,
            timestamp__year=current_year
        )

    # Default / Refresh / Archive untick → current month
    else:
        records = records.filter(
            timestamp__month=current_month,
            timestamp__year=current_year
        )

    grouped_records = defaultdict(list)

    for record in records:
        date = record.timestamp.date()
        grouped_records[date].append(record)

    attendance_data = []

    total_portion = 0
    total_minutes = 0
    total_late = 0

    for date, recs in grouped_records.items():

        clock_in = None
        clock_out = None
        status = "SR"
        total_hours = "0h 00m"
        late_status = "--"

        # Weekly Off (Sunday)
        if date.weekday() == 6:
            status = "WO"

        # Public Holiday
        if str(date) in PUBLIC_HOLIDAYS:
            status = "PH"

        if len(recs) >= 1:
            clock_in = recs[0]

            if clock_in.timestamp.time() >= time(11, 0):
                late_status = "1"

        if late_status == "1":
            total_late += 1

        if len(recs) >= 2:

            clock_out = recs[1]

            diff = clock_out.timestamp - clock_in.timestamp
            total_seconds = int(diff.total_seconds())

            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60

            total_hours = f"{hours}h {minutes:02d}m"

            total_minutes += (hours * 60 + minutes)

            # Full Day
            if hours >= 9:
                status = "DP"

            # Half Day
            elif hours >= 4:
                status = "HD"

            # Absent
            else:
                status = "DA"

        attendance_data.append({
            "date": date,
            "clock_in": clock_in,
            "clock_out": clock_out,
            "status": status,
            "total_hours": total_hours,
            "late": late_status
        })

        total_portion += 1

    total_hours_sum = f"{total_minutes // 60}h {total_minutes % 60:02d}m"

    context = {
        "records": attendance_data,
        "total_portion": total_portion,
        "total_hours_sum": total_hours_sum,
        "total_late": total_late
    }

    return render(
        request,
        "my_attendance_application/my_attendance_home.html",
        context
    )