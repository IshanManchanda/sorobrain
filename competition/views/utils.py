import json

from django.db import DatabaseError
from django.template.loader import render_to_string
from django.core.mail import send_mail

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
	try:
		CompetitionAccess.objects.get(user=user, competition=competition)
		return True
	except CompetitionAccess.DoesNotExist:
		return False


def generate_competition_codes(competition: Competition, number_of_codes: int) -> list:
	codes = []
	for _ in range(number_of_codes):
		cc = CompetitionCode(uses=1, expiry_date=competition.start_date, competition=competition)
		cc.save()
		codes.append(cc.code)
	return codes


def send_certificate(competition: Competition, user: User):
	rank = list(json.loads(competition.result).keys()).index(user.username) + 1  # index at 1
	html = render_to_string('competition/competition_certificate.html',
	                        {'competition': competition,
	                         'user'       : user,
	                         'rank'       : rank})
	send_mail('Competition Certificate', 'Certificate',
	          from_email='sorobrain.devs@gmail.com',
	          recipient_list=[user.email], fail_silently=False,
	          html_message=html)
