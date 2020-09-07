import json
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import DatabaseError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.core.files import File

from weasyprint import HTML

from competition.models.competition import Competition, CompetitionCertificate
from competition.models.store import CompetitionAccess, CompetitionCode
from main.models import User
from main.views.utils import grant_book_access


def grant_access_to_competition(user: User, competition: Competition) -> bool:
	try:
		CompetitionAccess.objects.create(user=user, competition=competition)
		if competition.include_book:
			print("Here!")
			grant_book_access(user)
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
	png = HTML(string=html).write_png(presentational_hints=True)
	with tempfile.NamedTemporaryFile('w+b') as tmpfile:
		tmpfile.write(png)
		tmpfile.name = tmpfile.name + '.png'
		tmpfile.seek(0)
		cc = CompetitionCertificate(competition=competition,
		                            user=user,
		                            certificate=SimpleUploadedFile(name=tmpfile.name,
		                                                           content=tmpfile.read()))
		cc.save()

		html_message = render_to_string('competition/certificate_email.html',
		                                {'cc': cc})
		print(html_message)
		send_mail('Competition Certificate', 'Certificate',
		          from_email='sorobrain.devs@gmail.com',
		          recipient_list=[user.email], fail_silently=False,
		          html_message=html_message)
