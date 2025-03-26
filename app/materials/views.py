from django.shortcuts import render

# Create your views here.
def subjects(request):
	"""Render subjects list for materials"""
	return render(request, "materials/subjects.html")