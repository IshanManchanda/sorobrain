from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'quiz'

urlpatterns = [
	path('', TemplateView.as_view(template_name='quiz/index.html'), name='index'),


	# require staff
	path('question/<str:question_id>/', views.question, name='question')
]
