from django.contrib import messages
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View

from quiz.models import Quiz
from quiz.views.utils import has_access_to_quiz


class StartQuiz(View):
	@staticmethod
	def get(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		if not has_access_to_quiz(request.user, quiz):
			messages.add_message(request, messages.INFO, 'Please buy this quiz first, then try to attempt it!')
			return redirect(quiz.get_absolute_url())
		return render(request, 'quiz/attempt/start_quiz.html', {
			'quiz': quiz
		})

	@staticmethod
	def post(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		# TODO: Validate starting quiz and then logging start time etc.
		pass


class AttemptQuiz(View):
	@staticmethod
	def get(request, slug):
		pass


class CheckQuiz(View):
	@staticmethod
	def get(request, slug):
		pass
