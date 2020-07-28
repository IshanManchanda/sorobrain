from datetime import datetime

from django.contrib import messages
from django.db import DatabaseError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from main.models import User, BookAccess


def user_profile_setup_progress(user: User) -> int:
	"""
	Checks user data fields to determine the status of the users profile
	setup.
	:param user:
	:return: number of fields that are still empty
	"""
	empty_fields = 0
	if user.gender is None:
		empty_fields += 1
	if user.phone is None:
		empty_fields += 1
	# ignoring user.avatar as it is not essential for profile setup
	if user.education is None:
		empty_fields += 1
	if user.level is None:
		empty_fields += 1
	if user.school is None:
		empty_fields += 1
	if user.city is None:
		empty_fields += 1
	if user.country is None:
		empty_fields += 1
	if user.date_of_birth is None:
		empty_fields += 1

	return empty_fields


def is_profile_complete(user: User) -> bool:
	if user_profile_setup_progress(user) <= 0:
		return True
	else:
		return False


def block_if_profile_incomplete(request):
	if not is_profile_complete(request.user):
		messages.add_message(request, messages.WARNING, 'Please complete your profile to access this page')
		return redirect(reverse('settings'))


def grant_book_access(user: User) -> bool:
	"""
	Grant access to the book
	:param user:
	:return: returns False if error and True if success
	"""
	try:
		BookAccess.objects.create(user=user)
		return True
	except DatabaseError:
		return False


def has_book_access(user: User) -> bool:
	"""
	Checks if a user has access to the book
	:param user:
	:return:  returns False if doesn't have access and True if does
	"""
	if not user.is_authenticated:
		return False
	try:
		BookAccess.objects.get(user=user)
		return True
	except BookAccess.DoesNotExist:
		return False


def get_level_from_date_of_birth(dob):
	if dob is None or dob == '':
		return 'beginner'
	age = timezone.now().year - dob.year
	if age <= 12:
		return 'beginner'
	if 13 <= age <= 15:
		return 'intermediate'
	if age >= 16:
		return 'advanced'
