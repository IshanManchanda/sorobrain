import hashlib
import os
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from main.views.utils import grant_book_access, has_book_access
from sorobrain.utils import get_presigned_url
from workshops.models import Workshop


def index(request):
	return render(request, 'main/index.html', {
		'workshops': Workshop.objects.filter(active=True)
	})


class Book(View):
	@staticmethod
	def get(request):
		print(f'book access: {has_book_access(request.user)}')
		if request.user.is_authenticated and has_book_access(request.user):
			return redirect(get_presigned_url('book/lblr_manuscript.pdf'))
		return render(request, 'main/book.html', {})

	@staticmethod
	def post(request):
		amount = 1

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
		print(hash_text)
		print(str(hashlib.sha512(hash_text.encode('utf-8')).hexdigest()))
		if request.POST['hash'] != str(
				hashlib.sha512(hash_text.encode('utf-8')).hexdigest()):
			messages.add_message(request, messages.WARNING,
			                     "Err: 23; Invalid Hash")
			return redirect(reverse('payment_error'))

		grant_book_access(request.user)
		return redirect(reverse('book'))
