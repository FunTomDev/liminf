from django.shortcuts import render
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from materials.models import Material
from problems.models import Problem

# Create your views here.
def index(request):
    """Displays main page"""
    recent_materials = Material.objects.order_by('-uploaded_at')[:7]  # Fetch 7 latest materials
    recent_problems = Problem.objects.order_by('-uploaded_at')[:7]  # Fetch 7 latest problems

    context = {
        'recent_materials': recent_materials,
        'recent_problems': recent_problems,
    }
    return render(request, 'pages/index.html', context=context)

def about(request):
    """Displays about page"""
    return render(request, 'pages/about.html')

def donate(request):
    """Displays donate page"""
    return render(request, 'pages/donate.html')

def feedback(request):
    """Send feedback to author"""
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')

        if not email or not message:
            messages.error(request, "Wypełnij wszystkie pola.")
            return HttpResponseRedirect(reverse('home'))

        messages.success(request, "Wiadomość została pomyślnie wysłana. Dziękuję!")
        return HttpResponseRedirect(reverse('home'))

    return HttpResponseRedirect(reverse('home'))