import json
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View

from competition.models.competition import Competition
from competition.views.utils import has_access_to_competition
from quiz.models import Quiz, QuizSubmission
from quiz.views.utils import has_access_to_quiz


class StartCompetitionQuiz(LoginRequiredMixin, View):
	@staticmethod
	def get(request, competition_slug, quiz_slug):
		quiz = get_object_or_404(Quiz, slug=quiz_slug)
		competition = get_object_or_404(Competition, slug=competition_slug)
		if competition.is_in_progress:
			if has_access_to_competition(request.user, competition):
				if quiz in competition.quizzes.all():
					if competition.can_user_attempt_quiz(request.user, quiz):
						return render(request, 'quiz/attempt/start_competition_quiz.html', {
							'quiz': quiz, 'competition': competition})
					else:
						messages.add_message(request, messages.INFO, 'Please attempt the quizzes before this one to continue.')
						return redirect(competition.get_compete_url())
				else:
					messages.add_message(request, messages.INFO, 'Invalid Request, please try again.')
					return redirect(competition.get_absolute_url())
			else:
				messages.add_message(request, messages.INFO, 'Register for this compete first!')
				return redirect(competition.get_absolute_url())
		messages.add_message(request, messages.INFO, 'Competition is no longer in progress')
		return redirect(competition.get_compete_url())

	@staticmethod
	def post(request, competition_slug, quiz_slug):
		quiz = get_object_or_404(Quiz, slug=quiz_slug)
		competition = get_object_or_404(Competition, slug=competition_slug)
		try:
			qs = QuizSubmission.objects.get(user=request.user, quiz=quiz, competition=competition)
			qs.start_time = timezone.now()
			qs.save()
		except QuizSubmission.DoesNotExist:
			qs = QuizSubmission.objects.create(
					user=request.user, quiz=quiz, competition=competition,
					start_time=timezone.now() + timedelta(seconds=5))
		if qs.score is not None:
			messages.add_message(request, messages.WARNING, 'You have already submitted this quiz!')
			return redirect(competition.get_compete_url())

		return redirect(quiz.get_attempt_url(qs))


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
		# give the user an extra minute to account for any delay in starting
		qs = QuizSubmission.objects.create(
				user=request.user, quiz=quiz,
				start_time=timezone.now())

		return redirect(quiz.get_attempt_url(qs))


class AttemptQuiz(LoginRequiredMixin, View):
	@staticmethod
	def get(request, quiz_slug, quiz_submission_id):
		quiz = get_object_or_404(Quiz, slug=quiz_slug)
		qs = get_object_or_404(QuizSubmission, id=quiz_submission_id)

		# validation
		if qs.score is not None:
			messages.add_message(request, messages.INFO,
			                     'Please start over here')
			return redirect(quiz.get_start_url())
		if not has_access_to_quiz(request.user, quiz):
			messages.add_message(request, messages.INFO,
			                     'Please buy this quiz first, then try to attempt it!')
			return redirect(quiz.get_absolute_url())
		if qs.submit_time:
			messages.add_message(request, messages.WARNING, 'This quiz has already been submitted, please start it again!')
			return redirect(quiz.get_absolute_url())

		return render(request, 'quiz/attempt/attempt.html', {
			'quiz'           : quiz,
			'quiz_submission': qs
		})

	@staticmethod
	def post(request, quiz_slug, quiz_submission_id):
		qs = get_object_or_404(QuizSubmission, id=quiz_submission_id)
		qs.submission = request.POST['quiz_state']
		qs.save()

		return HttpResponse(status=204)


class CheckQuiz(View):
	@staticmethod
	def get(request, quiz_slug, quiz_submission_id):
		quiz = get_object_or_404(Quiz, slug=quiz_slug)
		qs = get_object_or_404(QuizSubmission, id=quiz_submission_id)

		return render(request, 'quiz/attempt/checked.html', {
			'quiz'  : quiz,
			'result': qs.get_result(),
			'qs': qs
		})

	@staticmethod
	def post(request, quiz_slug, quiz_submission_id):
		quiz = get_object_or_404(Quiz, slug=quiz_slug)
		qs = get_object_or_404(QuizSubmission, id=quiz_submission_id)

		qs.submit_time = timezone.now() - timedelta(seconds=2)
		qs.submission = request.POST['quiz_state']
		qs.save()

		qs.check_and_score()

		return HttpResponse(status=204)
