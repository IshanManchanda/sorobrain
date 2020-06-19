from django.shortcuts import render

from quiz.models import Quiz
from workshops.models import Workshop


def catalog(request):
	return render(request, 'main/catalog.html', {
		'workshops': Workshop.objects.filter(active=True),
		'quizzes': Quiz.objects.filter(active=True)
	})
