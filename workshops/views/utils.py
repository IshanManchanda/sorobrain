from main.models import User
from workshops.models import WorkshopAccess, Workshop


def has_access_to_workshop(user: User, workshop: Workshop) -> bool:
	"""Checks the WorkshopAccess table with the user and workshop"""
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
