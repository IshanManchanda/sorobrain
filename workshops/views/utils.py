from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse

from main.models import User
from workshops.models import WorkshopAccess, Workshop


def grant_access_to_workshop(user: User, workshop: Workshop):
	"""Grant access to a workshop by creating a WorkshopAccess object,
	returns true for success and redirects to payment_error if failed"""
	try:
		WorkshopAccess.objects.create(user=user, workshop=workshop)
		return True
	except DatabaseError:
		return redirect(reverse('payment_error'))


def has_access_to_workshop(user: User, workshop: Workshop) -> bool:
	"""Checks the WorkshopAccess table with the user and workshop"""
	if user.is_authenticated:
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
