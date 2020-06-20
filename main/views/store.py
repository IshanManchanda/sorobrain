from django.shortcuts import render
from django.utils import timezone

from competition.models import Competition
from quiz.models import Quiz
from workshops.models import Workshop


def catalog(request):
	return render(request, 'main/catalog.html', {
		'competitions': Competition.objects.filter(active=True, end_date__lt=timezone.now()),
		'workshops': Workshop.objects.filter(active=True),
		'quizzes': Quiz.objects.filter(active=True),
	})
