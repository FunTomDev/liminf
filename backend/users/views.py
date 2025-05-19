from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST

from .forms import StudentCreationForm, StudentLoginForm

from materials.models import Material
from problems.models import Problem

# Create your views here.
def profile_view(request):
    """Used to display user profile"""

    uploaded_materials = Material.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')
    uploaded_problems = Problem.objects.filter(uploaded_by=request.user).order_by('-uploaded_at')

    context = {
        'uploaded_materials': uploaded_materials,
        'uploaded_problems': uploaded_problems,
    }

    return render(request, 'users/profile.html', context=context)

def login_view(request):
    """Used for user authentication"""

    if request.method == 'POST':
        form = StudentLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return HttpResponseRedirect(reverse('home'))
    else:
        form = StudentLoginForm()
    
    return render(request, 'users/login.html', {'form': form})

@require_POST
def logout_view(request):
    """Used for user logout"""
    logout(request)
    return HttpResponseRedirect(reverse('home'))

def registration_view(request):
    """Used for user registration"""

    if request.method == 'POST':
        form = StudentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Konto zostało utworzone pomyślnie. Możesz się teraz zalogować.")
            return HttpResponseRedirect(reverse('users:login'))
        print("Form is not valid", form.errors)
    else:
        form = StudentCreationForm()
    return render(request, 'users/register.html', {'form': form})

def reset_password(request):
    """Used to reset password"""
    return render(request, "users/reset-password.html")