from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'users'
urlpatterns = [

	path("login/", views.login_view, name = 'login'),
	path("register/", views.registration_view, name = 'register'),
    path("profile/", views.profile_view, name = 'profile'),
    path("logout/", views.logout_view, name = 'logout'),
	path("reset-password/", views.reset_password, name = 'reset-password'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)