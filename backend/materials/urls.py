from django.urls import path, include
from . import views

app_name = "materials"
urlpatterns = [

	path("", views.materials, name = "list"),
	path("<slug:subject_slug>/<slug:topic_slug>/<int:material_id>/", views.details, name="details"),
    path('ajax/', views.materials_ajax, name='materials_ajax'),
    path('add', views.add_material, name='add'),
    path('<int:material_id>/edit', views.edit_material, name='edit'),
    path('<int:material_id>/delete', views.delete_material, name='delete'),

]