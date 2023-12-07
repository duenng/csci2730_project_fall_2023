from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect

def please(request):
    return render(request, "please.html")

def logout_view(request):
    logout(request)
    return redirect('home') 

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect after successful registration
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form, 'active_page': 'register'})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page.
            else:
                # Return an 'invalid login' error message
                form.add_error(None, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()

    return render(request, 'registration/login.html', {'form': form, 'active_page': 'login'})
