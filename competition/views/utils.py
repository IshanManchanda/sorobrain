from django.db import DatabaseError

from competition.models.competition import Competition
from competition.models.store import CompetitionAccess, CompetitionCode
from main.models import User


def grant_access_to_competition(user: User, competition: Competition) -> bool:
	try:
		CompetitionAccess.objects.create(user=user, competition=competition)
		return True
	except DatabaseError:
		return False


def has_access_to_competition(user: User, competition: Competition) -> bool:
	if not user.is_authenticated:
		return False
	if competition.cost > 0:
		try:
			CompetitionAccess.objects.get(user=user, competition=competition)
			return True
		except CompetitionAccess.DoesNotExist:
			return False
	else:
		return True


def generate_competition_codes(competition: Competition, number_of_codes: int) -> list:
	codes = []
	for _ in range(number_of_codes):
		cc = CompetitionCode(uses=1, expiry_date=competition.start_date, competition=competition)
		cc.save()
		codes.append(cc.code)
	return codes
