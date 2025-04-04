from django.urls import path, include
from . import views

app_name = "materials"
urlpatterns = [

	path("", views.subjects, name = "subjects-list"),
	path("<slug:subject_slug>/<slug:topic_slug>/<int:material_id>/", views.details, name="details"),

]