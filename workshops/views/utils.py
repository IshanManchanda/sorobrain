import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.mail import send_mail
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse

from weasyprint import HTML

from main.models import User, BookAccess
from main.views.utils import grant_book_access
from workshops.models import WorkshopAccess, Workshop
from workshops.models.models import WorkshopCertificate


def grant_access_to_workshop(user: User, workshop: Workshop):
	"""Grant access to a workshop by creating a WorkshopAccess object,
	returns true for success and redirects to payment_error if failed
	Also if the workshop includes the book, it will also grant access to
	the book.
	"""
	try:
		WorkshopAccess.objects.create(user=user, workshop=workshop)
		if workshop.include_book:
			try:
				grant_book_access(user)
			except DatabaseError:
				return False
		return True
	except DatabaseError:
		return redirect(reverse('payment_error'))


def has_access_to_workshop(user: User, workshop: Workshop) -> bool:
	"""Checks the WorkshopAccess table with the user and workshop"""
	if not user.is_authenticated:
		return False
	try:
		WorkshopAccess.objects.get(user=user, workshop=workshop)
		return True
	except WorkshopAccess.DoesNotExist:
		return False


def get_workshop_amount(workshop: Workshop) -> int:
	"""Calculates the total amount for workshop with discount"""
	base = workshop.cost
	discount = workshop.discount
	if discount is None:
		return base
	return int(base * (100-discount))


def send_certificate(workshop: Workshop, user: User):
	html = render_to_string('workshops/workshop_certificate.html', {
		'workshop': workshop,
		'user': user
	})
	png = HTML(string=html).write_png(presentational_hints=True)
	with tempfile.NamedTemporaryFile('w+b') as tmpfile:
		tmpfile.write(png)
		tmpfile.name = tmpfile.name + 'png'
		tmpfile.seek(0)
		wc = WorkshopCertificate(workshop=workshop, user=user,
		                         certificate=SimpleUploadedFile(name=tmpfile.name,
		                                                        content=tmpfile.read()))
		wc.save()

		html_message = render_to_string('workshops/certificate_email.html',
		                                {'wc': wc})
		send_mail(f'eCertificat du concours « {workshop.title} »', 'Certificate',
		          from_email='sorobrain.devs@gmail.com',
		          recipient_list=[user.email], fail_silently=False,
		          html_message=html_message)
