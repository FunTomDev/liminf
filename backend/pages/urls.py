from django.urls import path, include
from . import views

urlpatterns = [

	path('', views.index, name = 'home'),
	path('materials/', include('materials.urls')),
	path('', include('users.urls')),
	path('problems/', include("problems.urls"), name = 'problems'),
	path('about/', views.about, name = 'about'),
	path('donate/', views.donate, name = 'donate'),
	path('feedback/', views.feedback, name = 'feedback'),

]