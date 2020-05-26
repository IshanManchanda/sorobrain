from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'workshops'

urlpatterns = [
	path('', TemplateView.as_view(template_name='workshops/index.html'), name='index'),
]
