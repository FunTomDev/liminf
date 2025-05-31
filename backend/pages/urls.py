from django.urls import path, include
from . import views

urlpatterns = [

	path('curriculum/', include('curriculum.urls')),
	path('materials/', include('materials.urls'), name = 'materials'),
	path('problems/', include("problems.urls"), name = 'problems'),
	path('', views.index, name = 'home'),
	path('about/', views.about, name = 'about'),
	path('feedback/', views.feedback, name = 'feedback'),
	path('', include('users.urls')),

]