from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
            
        else:
            return render(request, 'authentication/user_login.html', {
                'error': 'Invalid username or password.'
            })

    return render(request, 'authentication/user_login.html')

@login_required
def home(request):
    return render(request, 'authentication/home.html')

@login_required
def id_card(request):
    return render(request, 'authentication/id_card.html')

@login_required
def profile(request):
    return render(request, 'authentication/profile.html')

def logout_view(request):
    logout(request)
    return redirect('user_login')
