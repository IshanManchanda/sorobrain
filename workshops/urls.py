from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from . import views
from .models import Workshop

app_name = 'workshops'

urlpatterns = [
	path('', ListView.as_view(template_name='workshops/index.html', model=Workshop), name='index'),
	path('success/<str:slug>/', csrf_exempt(views.WorkshopSuccess.as_view()), name='payment_success'),
	path('code/<str:slug>/', views.RegisterWithCode.as_view(), name='register_with_code'),
	path('info/<str:slug>/', views.WorkshopStore.as_view(), name='workshop_store'),
	path('access/<str:slug>/', views.HasAccessWorkshop.as_view(), name='workshop_access'),
	path('send/<str:slug>/', views.SendCertificates.as_view(), name='send_certificate'),
	path('certificates/<str:slug>/<str:username>/', views.Certificate.as_view(), name='certificate')
]
