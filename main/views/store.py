from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View, generic

from competition.models import Competition
from main.models import OneOnOneClass
from main.views.utils import block_if_profile_incomplete, user_profile_setup_progress
from quiz.models import Quiz
from workshops.models import Workshop


def catalog(request):
	empty_fields = user_profile_setup_progress(request.user)
	if empty_fields > 0:
		messages.add_message(request, messages.INFO,
		                     f"Finish setting up your profile <a href={reverse('settings')}> here</a>. You have {empty_fields} fields to fill.")
		return redirect(reverse('settings'))

	return render(request, 'main/catalog.html', {
		'competitions': Competition.objects.filter(active=True).order_by('-created_on'),
		'workshops'   : Workshop.objects.filter(active=True).order_by('-created_on'),
		'quizzes'     : Quiz.objects.filter(active=True).order_by('-created_on'),
		'classes'     : OneOnOneClass.objects.filter(active=True).order_by('-created_on'),
		'new_competitions': Competition.get_recent(),
		'new_quizzes': Quiz.get_recent(),
		'new_workshops': Workshop.get_recent(),
	})


class ViewAllCompetitions(View):
	@staticmethod
	def get(request):
		queryset = Competition.objects.filter(active=True)
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
		queryset = Quiz.objects.filter(active=True)
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
		queryset = Workshop.objects.filter(active=True)
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
