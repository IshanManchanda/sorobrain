from django.db import DatabaseError

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

	return empty_fields


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
