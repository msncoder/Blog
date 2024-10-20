



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login  # Correctly imported as auth_login
from django.contrib.auth import logout as auth_logout  # Import logout without conflict
# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        initial_data = {'username': '', 'password1': '', 'password2': ''}
        form = UserCreationForm(initial=initial_data)
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)  # Use the renamed login function
            return redirect('index')
    else:
        initial_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial=initial_data)

    return render(request, 'auth/login.html', {'form': form})

def user_logout(request):  # Renamed logout view to avoid conflict
    auth_logout(request)  # Use the correctly imported logout
    return redirect('index')


def dashboard(request):
    pass
