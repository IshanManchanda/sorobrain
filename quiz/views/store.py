from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import mail_managers
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views import View
from django.utils import timezone
from django.views.generic import TemplateView

from main.models.code import DiscountCode
from quiz.models import Quiz, QuizCode
from quiz.views.utils import has_access_to_quiz, grant_access_to_quiz
from sorobrain.utils.utils import send_product_bought_mail, add_ledger_debit
from workshops.froms import RegisterWithCodeForm


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
		mail_managers(
				'[eSorobrain.com] New Quiz Registered',
				f'{request.user.username}: {request.user.name} with email: {request.user.email} has bought quiz: {quiz.title} at {timezone.now()}.',
				fail_silently=True
		)

		msg = render_to_string('mails/txt/product_bought.txt',
		                       {'user'        : request.user,
		                        'content_type': 'quiz', 'product': quiz})
		msg_html = render_to_string('mails/html/product_bought.html',
		                            {'user'        : request.user,
		                             'content_type': 'quiz',
		                             'product'     : quiz})
		send_product_bought_mail('[Sorobrain] New Quiz Registered',
		                         msg, msg_html, to=[request.user.email])
		return redirect(quiz.get_absolute_url())


class RegisterWithCode(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		form = RegisterWithCodeForm()
		return render(request, 'quiz/store/register_with_code.html', {
			'quiz': quiz,
			'form': form
		})

	@staticmethod
	def post(request, slug):
		quiz = get_object_or_404(Quiz, slug=slug)
		form = RegisterWithCodeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			code = get_object_or_404(QuizCode, code=data['code'])
			if code.is_valid(quiz):
				grant_access_to_quiz(request.user, quiz)
				code.use()
			else:
				messages.add_message(request, messages.WARNING,
				                     "Error 12: That code is invalid")
				return redirect(
					reverse('competition:code', args=[slug]))
			messages.add_message(request, messages.SUCCESS,
			                     "Registered Successfully")
			return redirect(quiz.get_absolute_url())
		messages.add_message(request, messages.INFO, "That code is invalid")
		return redirect(reverse('competition:code', args=[slug]))


class RegisterWithPoints(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		return redirect(reverse('quiz:buy', args=[slug]))

	@staticmethod
	def post(request, slug):
		q = get_object_or_404(Quiz, slug=slug)
		if request.user.points >= q.sub_total:
			request.user.points -= q.sub_total
			request.user.save()
			add_ledger_debit(request.user, q.sub_total, f"Bought Quiz {q.title}")
			grant_access_to_quiz(request.user, q)
			mail_managers(
					'[eSorobrain.com] New Quiz Registered with Soromoney.',
					f'{request.user.username}: {request.user.name} with email: {request.user.email} has bought quiz: {q.title} at {timezone.now()} with Soromoney.',
					fail_silently=True
			)
		else:
			messages.add_message(request, messages.WARNING,
			                     "You don't have enough points to register for this quiz!")
			return redirect(reverse('quiz:buy', args=[slug]))
		messages.add_message(request, messages.SUCCESS, "Success! You now have access to the quiz!")
		return redirect(reverse('quiz:start', args=[slug]))
