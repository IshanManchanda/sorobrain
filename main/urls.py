from django.urls import path
from django.views.generic import TemplateView

from . import views

# TODO: Test Google OAuth2

urlpatterns = [

	# account
	path('accounts/profile/', views.Profile.as_view(), name='profile'),
	path('accounts/settings/', views.Settings.as_view(), name='settings'),
	path('accounts/delete/', views.Delete.as_view(), name='delete'),
	path('accounts/save_profile/', views.SaveProfileData.as_view(), name='save_profile'),
	path('accounts/save_notification', views.SaveNotificationLevel.as_view(), name='save_notifications'),
	path('register/', views.register, name='register'),

	path('', views.index, name='index'),
]
