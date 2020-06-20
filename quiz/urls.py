from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from . import views

app_name = 'quiz'

urlpatterns = [
	# store
	path('', views.Index.as_view(), name='index'),
	path('buy/<str:slug>/', views.BuyQuiz.as_view(), name='buy'),
	path('success/<str:slug>/', csrf_exempt(views.QuizPaymentSuccess.as_view()), name='success'),

	# attempts
	path('compete/start/<str:competition_slug>/<str:quiz_slug>/', views.StartCompetitionQuiz.as_view(), name='competition_start'),
	path('start/<str:slug>/', views.StartQuiz.as_view(), name='start'),
	path('q/<str:quiz_slug>/<int:quiz_submission_id>/', views.AttemptQuiz.as_view(), name='attempt'),
	path('q/checked/<str:quiz_slug>/<int:quiz_submission_id>/', views.CheckQuiz.as_view(), name='check'),

	# require staff
	path('question/<int:question_id>/', views.question, name='question')
]
