import hashlib
import os
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from main.models import OneOnOneClass
from main.views.utils import grant_book_access, has_book_access, block_if_profile_incomplete, \
	user_profile_setup_progress
from sorobrain.utils import get_presigned_url
from workshops.models import Workshop


def index(request):
	empty_fields = user_profile_setup_progress(request.user)
	if empty_fields > 0:
		messages.add_message(request, messages.INFO,
		                     f"Finish setting up your profile <a href={reverse('settings')}> here</a>. You have {empty_fields} fields to fill.")
		return redirect(reverse('settings'))
	return render(request, 'main/index.html', {
		'workshops': Workshop.objects.filter(active=True)
	})


class Book(View):
	@staticmethod
	def get(request):
		block_if_profile_incomplete(request)
		if request.user.is_authenticated and has_book_access(request.user):
			return redirect(get_presigned_url('book/lblr_manuscript.pdf'))
		return render(request, 'main/book.html', {})

	@staticmethod
	def post(request):
		amount = 226

		if not request.user.is_authenticated:
			messages.add_message(request, messages.WARNING,
			                     "You need to login before you can buy something!")
			return redirect(reverse('account_login'))

		data = {
			'merchant_key': os.environ.get('PAYU_MERCHANT_KEY'),
			'txn_id'      : str(uuid4().hex),
			'amount'      : int(amount),
			'product_info': 'Le Bleu ou La Rose',
			'first_name'  : request.user.name.split(' ', 1)[0],
			'email_id'    : request.user.email,
			'phone_number': str(request.user.phone),
			'surl'        : request.build_absolute_uri(
					reverse('book_success')),
			'furl'        : request.build_absolute_uri(
					reverse('payment_error'))
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

		return JsonResponse(data)


class BookSuccess(LoginRequiredMixin, View):
	@staticmethod
	def post(request):
		hash_text = "%s|%s|||||||||||%s|%s|%s|%s|%s|%s" % (
			os.environ.get('PAYU_MERCHANT_SALT'),
			request.POST['status'],
			request.POST['email'],
			request.POST['firstname'],
			request.POST['productinfo'],
			request.POST['amount'],
			request.POST['txnid'],
			request.POST['key'],
		)
		if request.POST['hash'] != str(
				hashlib.sha512(hash_text.encode('utf-8')).hexdigest()):
			messages.add_message(request, messages.WARNING,
			                     "Err: 23; Invalid Hash")
			return redirect(reverse('payment_error'))

		grant_book_access(request.user)
		return redirect(reverse('book'))


class ClassStore(View):
	@staticmethod
	def get(request, slug):
		c = get_object_or_404(OneOnOneClass, slug=slug)
		return render(request, 'main/class.html', {'class': c})
