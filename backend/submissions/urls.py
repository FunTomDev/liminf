from django.urls import path, include
from . import views

app_name = "submissions"
urlpatterns = [
    
	path("solutions/<int:solution_id>", views.solution, name="details"),
    path("solutions/add", views.add_solution, name="add"),
    path("solutions/toggle_helpful", views.toggle_helpful_solution, name="toggle-helpful"),
    path('solutions/ajax/<int:solution_id>/', views.ajax_solution_detail, name='ajax-solution-detail'),

]
