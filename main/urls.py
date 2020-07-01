from django.urls import path
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt

from . import views


urlpatterns = [

	# account
	path('accounts/profile/', views.Profile.as_view(), name='profile'),
	path('accounts/settings/', views.Settings.as_view(), name='settings'),
	path('accounts/delete/', views.Delete.as_view(), name='delete'),
	path('accounts/save_profile/', views.SaveProfileData.as_view(), name='save_profile'),
	path('accounts/save_notification', views.SaveNotificationLevel.as_view(), name='save_notifications'),
	path('register/', views.register, name='register'),

	path('class/<str:slug>/', views.ClassStore.as_view(), name='class'),

	path('book/', views.Book.as_view(), name='book'),
	path('book/success/', csrf_exempt(views.BookSuccess.as_view()), name='book_success'),

	path('privacy/', TemplateView.as_view(template_name='main/privacy.html'), name='privacy'),
	path('refund/', TemplateView.as_view(template_name='main/refund.html'), name='refund'),
	path('catalog/', views.catalog, name='catalog'),
	path('contact/', TemplateView.as_view(template_name='main/contact.html'), name='contact'),
	path('global/', TemplateView.as_view(template_name='main/global.html'), name='global'),
	path('faq/', TemplateView.as_view(template_name='main/faq.html'), name='faq'),
	path('', views.index, name='index'),
]
