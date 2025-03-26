from django.shortcuts import render

# Create your views here.
def index(request):
	"""Displays main page"""
	return render(request, 'pages/index.html')

def problems(request):
	"""Displays problems subpage"""
	return render(request, 'pages/problems.html')

def about(request):
	"""Displays about page"""
	return render(request, 'pages/about.html')

def donate(request):
	"""Displays donate page"""
	return render(request, 'pages/donate.html')