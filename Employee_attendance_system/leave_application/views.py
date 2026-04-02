from django.shortcuts import render, redirect
from .forms import LeaveApplicationForm
from django.contrib.auth.decorators import login_required
from .models import LeaveApplication

# Create your views here.
def leave_home(request):
    return render(request, 'leave_application/leave_home.html')


@login_required
def leave_apply(request):
    if request.method == 'POST':
        form = LeaveApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.user = request.user
            leave.save()
            return redirect('leave_home')  # Replace with your actual view name
    else:
        form = LeaveApplicationForm()
    return render(request, 'leave_application/leave_apply.html', {'form': form})

@login_required
def recent_leave(request):
    applications = LeaveApplication.objects.filter(user=request.user).exclude(status__in=['approved', 'rejected']).order_by('-applied_at')
    return render(request, 'leave_application/recent_leave.html' , {'applications': applications})

@login_required
def approve_leave(request):
    applications = LeaveApplication.objects.filter(user=request.user).exclude(status__in=['pending', 'rejected']).order_by('-applied_at')
    return render(request, 'leave_application/approve_leave.html'  , {'applications': applications})

@login_required
def reject_leave(request):
    applications = LeaveApplication.objects.filter(user=request.user).exclude(status__in=['approved', 'pending']).order_by('-applied_at')
    return render(request, 'leave_application/reject_leave.html'  , {'applications': applications})

def lapsed_leave(request):
    return render(request, 'leave_application/lapsed_leave.html')