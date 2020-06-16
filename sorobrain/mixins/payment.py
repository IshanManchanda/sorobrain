import hashlib
import os
from uuid import uuid4

from django.contrib import messages
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse


class PaidObjectMixin(models.Model):
	"""Mixin that makes the object that inherits it payable, this
	makes the payment process stateless. """

	class Meta:
		abstract = True

	cost = models.IntegerField()
	discount = models.IntegerField(verbose_name='Discount Percentage',
	                               blank=True, null=True)

	@property
	def sub_total(self):
		if type(self.discount) == int and self.discount > 0:
			return int(self.cost * (1 - self.discount / 100))
		return self.cost

	def pay(self, request, amount, success_url, failure_url):
		"""
		This function takes a payment object and returns the JSON response
		required by the BOLT-PayU payment protocol.
		:param self:
		:param request: The request object from the view
		:param amount: This is explicit to allow for special pricing etc
		:param success_url: absolute url of view to redirect to on payment success
		:param failure_url: absolute url of view to redirect to on payment success
		:return: json response for BOLT
		"""
		login_url = request.build_absolute_uri(reverse('account_login'))

		if not request.user.is_authenticated:
			messages.add_message(request, messages.WARNING,
			                     "You need to login before you can buy something!")
			return redirect(login_url)

		product_info = self.title if not self.title == '' else 'no-product-info'

		data = {
			'merchant_key': os.environ.get('PAYU_MERCHANT_KEY'),
			'txn_id'      : str(uuid4().hex),
			'amount'      : int(amount),
			'product_info': product_info,
			'first_name'  : request.user.name.split(' ', 1)[0],
			'email_id'    : request.user.email,
			'phone_number': str(request.user.phone),
			'surl'        : success_url,
			'furl'        : failure_url
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

		# REVIEW: add some kind of logging here.
		# TODO: Add send customer and admin mail here

		return JsonResponse(data)

	@staticmethod
	def is_payment_valid(request):
		"""
		This method validates the payment by checking the hash sent from
		payu against a hash that it creates itself.
		:param request: the request object from the view
		:return: Returns a redirect if invalid hash, and a true if valid
		"""
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

		return True
