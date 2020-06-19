from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from main.models.code import DiscountCode
from workshops.models import Workshop, Code
from .utils import has_access_to_workshop, get_workshop_amount, \
	grant_access_to_workshop
from ..froms import RegisterWithCodeForm


class WorkshopStore(View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)

		if has_access_to_workshop(request.user, w):
			return redirect(reverse('workshops:workshop_access', args=[slug]))

		return render(request, 'workshops/workshop.html', {
			'workshop': w
		})

	@staticmethod
	def post(request, slug):
		w = get_object_or_404(Workshop, slug=slug)
		if w.is_expired:
			messages.add_message(request, messages.WARNING, "This workshop has expired")
			return redirect(reverse('workshops:workshop_store', args=[slug]))
		if request.POST['code'] != '':
			try:
				discount_code = DiscountCode.objects.get(
						code=request.POST['code'])
			except DiscountCode.DoesNotExist:
				messages.add_message(request, messages.WARNING, 'That discount code is not valid')
				return redirect(w.get_absolute_url())
		else:
			discount_code = ''
		return w.pay(request, amount=get_workshop_amount(w),
		             success_url=request.build_absolute_uri(
			             reverse('workshop:payment_success',
			                     args=[slug])),
		             failure_url=reverse('payment_error'),
		             code=discount_code)


class WorkshopSuccess(LoginRequiredMixin, View):
	@staticmethod
	def post(request, slug):
		w = get_object_or_404(Workshop, slug=slug)
		if w.is_payment_valid(request):
			grant_access_to_workshop(request.user, w)
		return redirect(reverse('workshops:workshop_store', args=[slug]))


class HasAccessWorkshop(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)

		if has_access_to_workshop(request.user, w):
			return render(request, 'workshops/has_access_workshop.html', {
				'workshop': w
			})
		return render(request, 'global/message.html', {
			'message_heading': 'No Permissions',
			'message'        : 'You do not have the permissions required to perform this action.'
		})


class RegisterWithCode(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)
		form = RegisterWithCodeForm()
		return render(request, 'workshops/register_with_code.html', {
			'workshop': w,
			'form': form
		})

	@staticmethod
	def post(request, slug):
		w = get_object_or_404(Workshop, slug=slug)
		form = RegisterWithCodeForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			code = get_object_or_404(Code, code=data['code'])
			if code.is_valid(w):
				grant_access_to_workshop(request.user, w)
				code.uses += -1
			else:
				messages.add_message(request, messages.WARNING, "Error 12: That code is invalid")
				return redirect(reverse('workshops:register_with_code', args=[slug]))
			messages.add_message(request, messages.SUCCESS, "Registered Successfully")
			return redirect(reverse('workshops:workshop_store', args=[slug]))
		messages.add_message(request, messages.INFO, "That code is invalid")
		return redirect(reverse('workshops:register_with_code', args=[slug]))
