from django.urls import path, include
from . import views

urlpatterns = [

	path('materials/', include('materials.urls')),
	path('problems/', include("problems.urls"), name = 'problems'),
	path('', views.index, name = 'home'),
	path('about/', views.about, name = 'about'),
	path('feedback/', views.feedback, name = 'feedback'),
	path('', include('users.urls')),

]