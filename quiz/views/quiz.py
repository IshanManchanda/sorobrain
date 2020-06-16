from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from quiz.models import Quiz, QuizSubmission
from quiz.views.utils import has_access_to_quiz


class StartQuiz(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		if not has_access_to_quiz(request.user, quiz):
			messages.add_message(request, messages.INFO,
			                     'Please buy this quiz first, then try to attempt it!')
			return redirect(quiz.get_absolute_url())
		return render(request, 'quiz/attempt/start_quiz.html', {
			'quiz': quiz
		})

	@staticmethod
	def post(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		# TODO: Check if quiz is part of a competition and perform appropriate validation.
		# give the user an extra minute to account for any delay in starting
		QuizSubmission.objects.create(
				user=request.user, quiz=quiz,
				start_time=timezone.now() + timedelta(seconds=60))

		return quiz.get_attempt_url()


class AttemptQuiz(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		if not has_access_to_quiz(request.user, quiz):
			messages.add_message(request, messages.INFO,
			                     'Please buy this quiz first, then try to attempt it!')
			return redirect(quiz.get_absolute_url())
		return render(request, 'quiz/attempt/attempt.html', {
			'quiz': quiz
		})

	@staticmethod
	def post(request, slug):
		# TODO: save the current quiz submission
		pass


class CheckQuiz(View):
	@staticmethod
	def get(request, slug):
		pass

	@staticmethod
	def post(request, slug):
		# TODO: update quiz submission object with submit time
		# TODO: check the quiz submission and return the score and analysis
		pass
