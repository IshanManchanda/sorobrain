from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse

from main.models import User, BookAccess
from main.views.utils import grant_book_access
from workshops.models import WorkshopAccess, Workshop


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
