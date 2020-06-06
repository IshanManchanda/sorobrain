from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

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

	path('book/', views.Book.as_view(), name='book'),
	path('book/success/', csrf_exempt(views.BookSuccess.as_view()), name='book_success'),

	path('catalog/', views.catalog, name='catalog'),
	path('contact/', TemplateView.as_view(template_name='main/contact.html'), name='contact'),
	path('', views.index, name='index'),
]
