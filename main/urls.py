from django.urls import path

from . import views

# TODO: Test Google OAuth2
# TODO: Add bootstrap

urlpatterns = [
	path('register/', views.register, name='register'),
	path('', views.index, name='index'),
]
