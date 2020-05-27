import hashlib
import os
from uuid import uuid4

from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from workshops.models import Workshop
from .utils import has_access_to_workshop, get_workshop_amount


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
		amount = get_workshop_amount(w)
		data = {
			'merchant_key': os.environ.get('PAYU_MERCHANT_KEY'),
			'txn_id'      : str(uuid4().hex),
			'amount'      : int(amount),
			'product_info': w.title,
			'first_name'  : request.user.name.split(' ', 1)[0],
			'email_id'    : request.user.email,
			'phone_number': str(request.user.phone),
			'surl'        : reverse('workshops:workshop_store', args=[slug]),
			'furl'        : reverse('index'),  # TODO: Update that <-
		}

		data['hash'] = str(hashlib.sha512(
				('%s|%s|%s|%s|%s|%s|||||||||||%s' % (
					data['merchant_key'],
					data['txn_id'],
					data['amount'],
					data['product_info'],
					data['first_name'],
					data['email_id'],
					os.environ.get('PAYU_MERCHANT_SALT')
				)).encode('utf-8')
		).hexdigest())

		# TODO: add some kind of logging here.
		# TODO: Add send customer and admin mail here

		return JsonResponse(data)


class HasAccessWorkshop(View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)

		if has_access_to_workshop(request.user, w):
			return render(request, 'workshops/has_access_workshop.html', {
				'workshop': w
			})
		return render(request, 'global/message.html', {
			'message_heading': 'No Permissions',
			'message'      : 'You do not have the permissions required to perform this action.'
		})
