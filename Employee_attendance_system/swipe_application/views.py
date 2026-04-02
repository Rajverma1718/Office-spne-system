from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SwipeApplicationForm
from .models import SwipeApplication


# Create your views here.
def swipe_home(request):
    return render(request, 'swipe_application/swipe_home.html')

@login_required
def swipe_apply(request):
    form = SwipeApplicationForm()
    user_requests = SwipeApplication.objects.filter(user=request.user).order_by('-applied_at')

    if request.method == 'POST':
        form = SwipeApplicationForm(request.POST)
        if form.is_valid():
            swipe = form.save(commit=False)
            swipe.user = request.user
            swipe.save()
            return redirect('swipe_apply')

    return render(request, 'swipe_application/swipe_apply.html', {'form': form,})


@login_required
def recent_swipe(request):
    applications = SwipeApplication.objects.filter(user=request.user).filter(status='pending').order_by('-applied_at')
    return render(request, 'swipe_application/recent_swipe.html', {'applications': applications})

@login_required
def approve_swipe(request):
    applications = SwipeApplication.objects.filter(user=request.user).filter(status='approved').order_by('-applied_at')
    return render(request, 'swipe_application/approve_swipe.html'  , {'applications': applications})

@login_required
def reject_swipe(request):
    applications = SwipeApplication.objects.filter(user=request.user).filter(status='rejected').order_by('-applied_at')
    return render(request, 'swipe_application/reject_swipe.html'  , {'applications': applications})

def lapsed_swipe(request):
    return render(request, 'swipe_application/lapsed_swipe.html')