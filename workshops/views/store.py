from datetime import datetime

from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, mail_managers
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from main.models import User
from main.models.code import DiscountCode
from sorobrain.utils.utils import send_product_bought_mail
from workshops.models import Workshop, Code, WorkshopAccess
from .utils import has_access_to_workshop, get_workshop_amount, \
	grant_access_to_workshop, send_certificate
from ..froms import RegisterWithCodeForm


class WorkshopStore(View):
	@staticmethod
	def get(request, slug):
		w = get_object_or_404(Workshop, slug=slug)

		if has_access_to_workshop(request.user, w):
			return redirect(reverse('workshops:workshop_access', args=[slug]))

		return render(request, 'workshops/workshop.html', {
			'workshop': w,
			'related': w.tags.similar_objects()
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

		return w.pay(request, amount=w.sub_total,
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
		mail_managers(
				'[eSorobrain.com] New Workshop Registered',
				f'{request.user.username}: {request.user.name} with email: {request.user.email} has bought workshop: {w.title} at {timezone.now()}.',
				fail_silently=True
		)

		msg = render_to_string('mails/txt/product_bought.txt', {'user': request.user, 'content_type': 'workshop', 'product': w})
		msg_html = render_to_string('mails/html/product_bought.html', {'user': request.user, 'content_type': 'workshop', 'product': w})
		send_product_bought_mail('[Sorobrain] New Workshop Registered', msg, msg_html, to=[request.user.email])

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
				code.use()
			else:
				messages.add_message(request, messages.WARNING, "Error 12: That code is invalid")
				return redirect(reverse('workshops:register_with_code', args=[slug]))
			messages.add_message(request, messages.SUCCESS, "Registered Successfully")
			return redirect(reverse('workshops:workshop_store', args=[slug]))
		messages.add_message(request, messages.INFO, "That code is invalid")
		return redirect(reverse('workshops:register_with_code', args=[slug]))


class SendCertificates(View, LoginRequiredMixin):
	@staticmethod
	def get(request, slug):
		if not request.user.is_staff:
			messages.add_message(request, messages.WARNING, 'Access not allowed')
			return redirect(reverse('index'))

		w = get_object_or_404(Workshop, slug=slug)
		users = [wa.user for wa in WorkshopAccess.objects.filter(workshop=w)]
		for u in users:
			send_certificate(w, u)
		return render(request, 'global/send_certificate.html', {'users': users})


class Certificate(View):
	"""
	The url for this view is 'certificate/<certificate_id>/<user_name>/'
	"""
	@staticmethod
	def get(request, slug, username):
		w = get_object_or_404(Workshop, slug=slug)
		user = get_object_or_404(User, username=username)
		return render(request, 'competition/compete/certificate.html', {
			'competition': w,
			'user': user
		})
