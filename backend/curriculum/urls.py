from django.urls import path, include
from . import views

app_name = 'curriculum'

urlpatterns = [
    path('topics/add/', views.add_topic, name='add_topic'),
    path('subjects/add/', views.add_subject, name='add_subject'),
    # Add more paths as needed for other views
]