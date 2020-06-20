from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from main.models.code import DiscountCode
from quiz.models import Quiz
from quiz.views.utils import has_access_to_quiz, grant_access_to_quiz


class Index(View):
	@staticmethod
	def get(request):
		return render(request, 'quiz/index.html', {
			'quizzes': Quiz.objects.filter(active=True)
		})


class BuyQuiz(View):
	@staticmethod
	def get(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)

		if has_access_to_quiz(request.user, quiz):
			return redirect(quiz.get_start_url())

		return render(request, 'quiz/store/buy.html', {
			'quiz': quiz
		})

	@staticmethod
	def post(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		if request.POST['code'] != '':
			try:
				discount_code = DiscountCode.objects.get(
						code=request.POST['code'])
			except DiscountCode.DoesNotExist:
				messages.add_message(request, messages.WARNING, 'That discount code is not valid')
				return redirect(quiz.get_absolute_url())
		else:
			discount_code = ''
		return quiz.pay(request, amount=quiz.sub_total,
		                success_url=request.build_absolute_uri(
			                reverse('quiz:success', args=[quiz.slug])),
		                failure_url=request.build_absolute_uri(
			                reverse('payment_error')),
		                code=discount_code)


class QuizPaymentSuccess(LoginRequiredMixin, View):
	@staticmethod
	def post(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		if quiz.is_payment_valid(request):
			grant_access_to_quiz(request.user, quiz)
		return redirect(quiz.get_absolute_url())
