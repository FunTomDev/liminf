from django.urls import path, include
from . import views

app_name = "problems"
urlpatterns = [

	path("", views.problems, name="list"),
	path("<slug:subject_slug>/<slug:topic_slug>/<int:problem_id>/", views.details, name="details"),
    path('ajax/', views.problems_ajax, name='ajax'),

]
