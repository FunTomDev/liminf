from django.shortcuts import render

# Create your views here.
def login(request):
	"""Used for user authentication"""
	return render(request, "users/login.html")

def register(request):
	"""Used for user registration"""
	return render(request, "users/register.html")

def reset_password(request):
	"""Used to reset password"""
	return render(request, "users/reset-password.html")