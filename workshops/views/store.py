import hashlib
import os
from uuid import uuid4

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from workshops.models import Workshop
from .utils import has_access_to_workshop, get_workshop_amount, \
	grant_access_to_workshop


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
		return w.pay(request, amount=get_workshop_amount(w),
		             success_url=reverse('workshop:payment_success',
		                                 args=[slug]),
		             failure_url=reverse('payment_error'))


class WorkshopSuccess(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)
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
