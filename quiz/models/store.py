from django.db import models
from django.db.models import QuerySet
from django.utils import timezone

from main.models import User
from quiz.models import Quiz


class QuizAccess(models.Model):
	class Meta:
		verbose_name = 'Quiz Access'
		verbose_name_plural = 'Quiz Access'
		unique_together = ('user', 'quiz')
		ordering = ('quiz', '-created_on')

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'user: {self.user} has access to {self.quiz}'
