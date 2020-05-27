from django.urls import path
from django.views.generic import ListView

from . import views
from .models import Workshop

app_name = 'workshops'

urlpatterns = [
	path('', ListView.as_view(template_name='workshops/index.html', model=Workshop), name='index'),
	path('info/<str:slug>/', views.WorkshopStore.as_view(), name='workshop_store'),
]
