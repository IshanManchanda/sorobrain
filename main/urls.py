from django.urls import path
from django.views.generic import TemplateView

from . import views

# TODO: Test Google OAuth2
# TODO: Add bootstrap

urlpatterns = [
	path('accounts/profile/', TemplateView.as_view(template_name='main/profile.html'), name='profile'),
	path('register/', views.register, name='register'),
	path('', views.index, name='index'),
]
