"""sorobrain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
	https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
	1. Add an import:  from my_app import views
	2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
	1. Add an import:  from other_app.views import Home
	2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URL conf
	1. Import the include() function: from django.urls import include, path
	2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.context_processors import static
from django.urls import path, include, re_path
from django.views.generic import TemplateView

from sorobrain import settings

admin.site.site_header = 'Sorobrain'

urlpatterns = [
	path('admin_tools/', include('admin_tools.urls')),
	path('admin/', admin.site.urls),
	re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
	path('accounts/', include('allauth.urls')),
	path('quiz/', include('quiz.urls', namespace='quiz')),
	path('workshop/', include('workshops.urls', namespace='workshop')),
	path('error/payment/', TemplateView.as_view(template_name='global/errors/payment.html'), name='payment_error'),
	path('', include('main.urls')),
]
