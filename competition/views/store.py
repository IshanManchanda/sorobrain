from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from competition.models.competition import Competition
from competition.models.store import CompetitionCode
from competition.views.utils import has_access_to_competition, \
	grant_access_to_competition, generate_competition_codes
from main.models.code import DiscountCode
from workshops.froms import RegisterWithCodeForm


class Index(View):
	@staticmethod
	def get(request):
		return render(request, 'competition/store/index.html', {
			'competitions': Competition.objects.filter(active=True)
		})


class BuyCompetition(View):
	@staticmethod
	def get(request, slug):
		competition = get_object_or_404(Competition, slug=slug)

		if has_access_to_competition(request.user, competition):
			return redirect(competition.get_compete_url())

		return render(request, 'competition/store/buy.html', {
			'competition': competition
		})

	@staticmethod
	def post(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		if request.POST['code'] != '':
			try:
				discount_code = DiscountCode.objects.get(code=request.POST['code'])
			except DiscountCode.DoesNotExist:
				messages.add_message(request, messages.WARNING, 'That discount code is not valid')
				return redirect(competition.get_absolute_url())
		else:
			discount_code = ''
		return competition.pay(request, amount=competition.sub_total,
		                       success_url=request.build_absolute_uri(reverse('competition:success', args=[competition.slug])),
		                       failure_url=request.build_absolute_uri(reverse('payment_error')),
		                       code=discount_code)


class CompetitionPaymentSuccess(LoginRequiredMixin, View):
	@staticmethod
	def post(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		if competition.is_payment_valid(request):
			grant_access_to_competition(request.user, competition)
		return redirect(competition.get_absolute_url())


class RegisterWithCode(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		form = RegisterWithCodeForm()
		return render(request, 'competition/store/register_with_code.html', {
			'competition': competition,
			'form': form
		})

	@staticmethod
	def post(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		form = RegisterWithCodeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			code = get_object_or_404(CompetitionCode, code=data['code'])
			if code.is_valid(competition):
				grant_access_to_competition(request.user, competition)
				code.uses += -1
			else:
				messages.add_message(request, messages.WARNING,
				                     "Error 12: That code is invalid")
				return redirect(
					reverse('competition:code', args=[slug]))
			messages.add_message(request, messages.SUCCESS,
			                     "Registered Successfully")
			return redirect(competition.get_absolute_url())
		messages.add_message(request, messages.INFO, "That code is invalid")
		return redirect(reverse('competition:code', args=[slug]))


class GroupBuyCompetition(View):
	@staticmethod
	def get(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		return render(request, 'competition/store/group_buy.html', {
			'competition': competition
		})

	@staticmethod
	def post(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		if request.POST['group_size'] != '':
			try:
				total_amount = competition.group_cost * abs(int(request.POST['group_size']))
			except TypeError:
				messages.add_message(request, messages.WARNING,
				                     'Group Size must be a positive integer')
				return redirect(reverse('competition:group_buy', args=[competition.slug]))
			return competition.pay(request, amount=total_amount,
			                       success_url=request.build_absolute_uri(
				                       reverse('competition:group_success',
				                               args=[competition.slug])),
			                       failure_url=request.build_absolute_uri(
				                       reverse('payment_error')),
			                       udf2=request.POST['group_size'])
		messages.add_message(request, messages.WARNING, 'Group Size is required!')
		return redirect(reverse('competition:group_buy', args=[competition.slug]))


class GroupPaymentSuccess(View):
	@staticmethod
	def post(request, slug):
		competition = get_object_or_404(Competition, slug=slug)
		if competition.is_payment_valid(request):
			codes = generate_competition_codes(competition, int(request.POST['udf2']))
			return render(request, 'competition/store/group_success.html', {
				'codes': codes,
				'competition': competition
			})
		else:
			return redirect(reverse('payment_error'))
