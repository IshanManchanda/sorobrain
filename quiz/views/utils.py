from sqlite3 import DatabaseError

from main.models import User
from quiz.models import Quiz, QuizAccess


def grant_access_to_quiz(user: User, quiz: Quiz) -> bool:
	try:
		QuizAccess.objects.create(user=user, quiz=quiz)
		return True
	except DatabaseError:
		return False


def has_access_to_quiz(user: User, quiz: Quiz) -> bool:
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
