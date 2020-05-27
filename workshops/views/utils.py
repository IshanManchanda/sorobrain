from main.models import User
from workshops.models import WorkshopAccess, Workshop


def has_access_to_workshop(user: User, workshop: Workshop):
	try:
		WorkshopAccess.objects.get(user=user, workshop=workshop)
		return True
	except WorkshopAccess.DoesNotExist:
		return False
