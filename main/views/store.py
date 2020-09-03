from django.shortcuts import render
from django.utils import timezone
from django.views import View, generic

from competition.models import Competition
from main.models import OneOnOneClass
from main.views.utils import block_if_profile_incomplete
from quiz.models import Quiz
from workshops.models import Workshop


def catalog(request):
	block_if_profile_incomplete(request)
	return render(request, 'main/catalog.html', {
		'competitions': Competition.objects.filter(active=True).order_by('-created_on'),
		'workshops'   : Workshop.objects.filter(active=True).order_by('-created_on'),
		'quizzes'     : Quiz.objects.filter(active=True).order_by('-created_on'),
		'classes'     : OneOnOneClass.objects.filter(active=True).order_by('-created_on')
	})


class ViewAllCompetitions(View):
	@staticmethod
	def get(request):
		print('hhh')
		queryset = Competition.objects.all()
		if request.GET.get('alphabetically') == 'true':
			queryset = queryset.order_by('-title')
		if request.GET.get('most_recent') == 'true':
			queryset = queryset.order_by('-created_on')
		if request.GET.get('oldest') == 'true':
			queryset = queryset.order_by('created_on')
		return render(request, 'main/all.html', {
			'object_type': 'Competitions',
			'objects': queryset
		})


class ViewAllQuizzes(View):
	@staticmethod
	def get(request):
		print('hhh')
		queryset = Quiz.objects.all()
		if request.GET.get('alphabetically') == 'true':
			queryset = queryset.order_by('-title')
		if request.GET.get('most_recent') == 'true':
			queryset = queryset.order_by('-created_on')
		if request.GET.get('oldest') == 'true':
			queryset = queryset.order_by('created_on')
		return render(request, 'main/all.html', {
			'object_type': 'Quizzes',
			'objects': queryset
		})


class ViewAllWorkshops(View):
	@staticmethod
	def get(request):
		print('hhh')
		queryset = Workshop.objects.all()
		if request.GET.get('alphabetically') == 'true':
			queryset = queryset.order_by('-title')
		if request.GET.get('most_recent') == 'true':
			queryset = queryset.order_by('-created_on')
		if request.GET.get('oldest') == 'true':
			queryset = queryset.order_by('created_on')
		return render(request, 'main/all.html', {
			'object_type': 'Workshops',
			'objects': queryset
		})
