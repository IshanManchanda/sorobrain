from sqlite3 import DatabaseError

from competition.models import CompetitionQuiz
from competition.views.utils import has_access_to_competition
from main.models import User
from quiz.models import Quiz, QuizAccess


def grant_access_to_quiz(user: User, quiz: Quiz) -> bool:
	try:
		QuizAccess.objects.create(user=user, quiz=quiz)
		return True
	except DatabaseError:
		return False


def has_access_to_quiz(user: User, quiz: Quiz) -> bool:
	if any([has_access_to_competition(user, cq.competition) for cq in CompetitionQuiz.objects.filter(quiz=quiz)]):
		return True
	if not user.is_authenticated:
		return False
	if quiz.cost > 0:
		try:
			QuizAccess.objects.get(user=user, quiz=quiz)
			return True
		except QuizAccess.DoesNotExist:
			return False
	else:
		return True
