import hashlib
import os
from uuid import uuid4

from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse

from main.models.code import DiscountCode


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

	def pay(self, request, amount, success_url, failure_url, code='', udf2=''):
		"""
		This function takes a payment object and returns the JSON response
		required by the BOLT-PayU payment protocol.
		:param self:
		:param request: The request object from the view
		:param amount: This is explicit to allow for special pricing etc
		:param success_url: absolute url of view to redirect to on payment success
		:param failure_url: absolute url of view to redirect to on payment success
		:param code: discount code for this payment
		:param udf2: anything you want to pass to the success view

		:return: json response for BOLT
		"""
		login_url = request.build_absolute_uri(reverse('account_login'))

		if not request.user.is_authenticated:
			messages.add_message(request, messages.WARNING,
			                     "You need to login before you can buy something!")
			return redirect(login_url)

		if code != '':
			if not code.is_used and not code.is_expired:
				if ContentType.objects.get_for_model(
						self) == code.content_type:
					if self.id == code.object_id:
						amount = amount * ((100 - code.discount) / 100)

		product_info = self.title if not self.title == '' else 'no-product-info'

		data = {
			'merchant_key': os.environ.get('PAYU_MERCHANT_KEY'),
			'txn_id'      : str(uuid4().hex),
			'amount'      : int(amount),
			'product_info': product_info,
			'first_name'  : request.user.name.split(' ', 1)[0],
			'email_id'    : request.user.email,
			'phone_number': str(request.user.phone),
			'udf1'        : code.code if code != '' else '',
			'udf2'        : udf2,
			'surl'        : success_url,
			'furl'        : failure_url
		}

		# key|txnid|amount|productinfo|firstname|email|udf1|udf2|||||||||salt;
		s = f"{data['merchant_key']}|{data['txn_id']}|{data['amount']}|{data['product_info']}|{data['first_name']}|{data['email_id']}|{data['udf1']}|{data['udf2']}|||||||||{os.environ.get('PAYU_MERCHANT_SALT')}"

		data['hash'] = str(hashlib.sha512(s.encode('utf-8')).hexdigest())

		return JsonResponse(data)

	@staticmethod
	def is_payment_valid(request):
		"""
		This method validates the payment by checking the hash sent from
		payu against a hash that it creates itself.
		:param request: the request object from the view
		:return: Returns a redirect if invalid hash, and a true if valid
		"""

		# salt|status|||||||||udf2|udf1|email|firstname|productinfo|amount|txnid|key
		s = f"{os.environ.get('PAYU_MERCHANT_SALT')}|{request.POST['status']}|||||||||{request.POST['udf2']}|{request.POST['udf1']}|{request.POST['email']}|{request.POST['firstname']}|{request.POST['productinfo']}|{request.POST['amount']}|{request.POST['txnid']}|{request.POST['key']}"
		hash_text = s

		if request.POST['hash'] != str(
				hashlib.sha512(hash_text.encode('utf-8')).hexdigest()):
			messages.add_message(request, messages.WARNING,
			                     "Err: 23; Invalid Hash")
			return redirect(reverse('payment_error'))

		code = request.POST['udf1']
		if code != '':
			DiscountCode.objects.get(code=code).use()

		return True
