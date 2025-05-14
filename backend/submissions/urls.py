from django.urls import path, include
from . import views

app_name = "submissions"
urlpatterns = [
    
	path("<slug:subject_slug>/<slug:topic_slug>/<int:problem_id>/solution/<int:solution_id>", views.solution, name="solution-details"),

]
