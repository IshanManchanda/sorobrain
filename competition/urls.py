from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from . import views

app_name = 'compete'

urlpatterns = [
	# store
	path('', views.Index.as_view(), name='index'),
	path('buy/<str:slug>/', views.BuyCompetition.as_view(), name='buy'),
	path('success/<str:slug>/', csrf_exempt(views.CompetitionPaymentSuccess.as_view()), name='success'),
	path('group_buy/<str:slug>/', views.GroupBuyCompetition.as_view(), name='group_buy'),
	path('group_success/<str:slug>/', csrf_exempt(views.GroupPaymentSuccess.as_view()), name='group_success'),
	path('code/<str:slug>/', views.RegisterWithCode.as_view(), name='code'),
	path('free/<str:slug>/', views.RegisterForFree.as_view(), name='free'),
	# compete
	path('compete/<str:slug>/', views.Compete.as_view(), name='compete'),
	path('result/<str:slug>/', views.Result.as_view(), name='result'),
	path('certificate/<str:slug>/<str:username>/', views.Certificate.as_view(), name='certificate'),
	path('send/<str:competition_slug>/', views.SendCertificates.as_view(), name='send_certificate')
]
