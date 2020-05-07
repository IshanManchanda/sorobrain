from django.urls import path

from . import views

# TODO: Create some basic views (index, etc.) or else server error
# TODO: Also favicon, etc
# TODO: Also create basic html pages
# TODO: Start creating custom forms
# TODO: Test Google OAuth2

# TODO: Add bootstrap

urlpatterns = [
	path('register/', views.register, name='register'),
	path('', views.index, name='index'),
]
