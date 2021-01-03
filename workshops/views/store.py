from datetime import datetime

from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail, mail_managers
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View

from main.models import User
from main.models.code import DiscountCode
from main.models.invoices import Invoice
from sorobrain.utils.utils import send_product_bought_mail, add_ledger_debit
from workshops.models import Workshop, Code, WorkshopAccess
from .utils import has_access_to_workshop, get_workshop_amount, \
	grant_access_to_workshop, send_certificate
from ..froms import RegisterWithCodeForm
from ..froms.certificates import SendCertificatesFormWorkshop


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

		invoice = Invoice(user=request.user, description=f"Workshop bought - {w.title}", amount=w.sub_total)
		invoice.save()
		msg = render_to_string('mails/txt/product_bought.txt', {'user': request.user, 'content_type': 'workshop', 'product': w})
		msg_html = render_to_string('mails/html/invoice.html', {'invoice': invoice})
		invoice.invoice_html = msg_html
		invoice.save()
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


class RegisterForFree(LoginRequiredMixin, View):
	@staticmethod
	def post(request, slug):
		workshop = get_object_or_404(Workshop, slug=slug)
		if not workshop.is_free:
			return HttpResponse(403)
		grant_access_to_workshop(request.user, workshop)
		mail_managers(
				'[eSorobrain.com] New Workshop Registered',
				f'{request.user.username}: {request.user.name} with email: {request.user.email} has bought workshop: {workshop.title} at {timezone.now()}.',
				fail_silently=True
		)
		messages.add_message(request, messages.SUCCESS, "You have successfully registered for the workshop! Please find it in the my registered workshops section.")
		return redirect(reverse('profile'))


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


class RegisterWithPoints(LoginRequiredMixin, View):
	@staticmethod
	def get(request, slug):
		return redirect(reverse('workshops:workshop_store', args=[slug]))

	@staticmethod
	def post(request, slug):
		w = get_object_or_404(Workshop, slug=slug)
		if request.user.points >= w.sub_total:
			request.user.points -= w.sub_total
			request.user.save()
			grant_access_to_workshop(request.user, w)
			add_ledger_debit(request.user, w.sub_total, f"Bought workshop {w.title}")
			mail_managers(
					'[eSorobrain.com] New Workshop Registered with Soromoney',
					f'{request.user.username}: {request.user.name} with email: {request.user.email} has bought workshop: {w.title} at {timezone.now()} with Soromoney.',
					fail_silently=True
			)
		else:
			messages.add_message(request, messages.WARNING, "You don't have enough points to register for this workshop!")
			return redirect(reverse('workshops:workshop_store', args=[slug]))
		messages.add_message(request, messages.SUCCESS, "Success! You now have access to the workshop!")
		return redirect(reverse('workshops:workshop_access', args=[slug]))


class SendCertificates(View, LoginRequiredMixin):
	@staticmethod
	def get(request, slug):
		if not request.user.is_staff:
			messages.add_message(request, messages.WARNING, 'Access not allowed')
			return redirect(reverse('index'))
		w = get_object_or_404(Workshop, slug=slug)
		form = SendCertificatesFormWorkshop(workshop=w)
		return render(request, 'workshops/send_certificate.html', {
			'form': form,
			'w': w
		})

	@staticmethod
	def post(request, slug):
		if not request.user.is_staff:
			messages.add_message(request, messages.WARNING, 'Access not allowed')
			return redirect(reverse('index'))

		w = get_object_or_404(Workshop, slug=slug)
		form = SendCertificatesFormWorkshop(request.POST, workshop=w)
		if form.is_valid():
			data = form.cleaned_data
			users = data['users']
			for u in users:
				send_certificate(w, u)
			messages.add_message(request, messages.SUCCESS, 'Certificates Sent!')
		else:
			messages.add_message(request, messages.WARNING, 'Invalid form data!')
		return redirect(reverse('workshops:send_certificate', args=[w.slug]))


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
