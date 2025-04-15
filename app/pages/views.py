from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from materials.models import Material
from submissions.models import Problem

# Create your views here.
def index(request):
    """Displays main page"""
    recent_materials = Material.objects.order_by('-uploaded_at')[:10]  # Fetch 10 latest materials
    recent_problems = Problem.objects.order_by('-uploaded_at')[:10]  # Fetch 10 latest problems

    context = {
        'recent_materials': recent_materials
    }
    return render(request, 'pages/index.html', context=context)

def problems(request):
    """Displays problems subpage"""
    return render(request, 'pages/problems.html')

def about(request):
    """Displays about page"""
    return render(request, 'pages/about.html')

def donate(request):
    """Displays donate page"""
    return render(request, 'pages/donate.html')

def feedback(request):
    """Send feedback to autor"""
    print(request.POST['email'])
    print(request.POST['message'])
    return HttpResponseRedirect(reverse('home'))