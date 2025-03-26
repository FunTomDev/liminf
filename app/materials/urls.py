from django.urls import path, include
from . import views

app_name = "materials"
urlpatterns = [

	path("", views.subjects, name = "subjects-list"),

]