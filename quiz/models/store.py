import string
from random import choice

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


class QuizCode(models.Model):
	class Meta:
		verbose_name = 'Quiz Code'
		verbose_name_plural = 'Quiz Codes'

	code = models.CharField(max_length=256, unique=True)
	uses = models.IntegerField()
	expiry_date = models.DateTimeField()
	quiz = models.ForeignKey('quiz.Quiz', on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(default=timezone.now)

	@property
	def is_used(self) -> bool:
		return self.uses <= 0

	@property
	def is_expired(self) -> bool:
		"""Returns true if the current time is after the education time"""
		return timezone.now() > self.expiry_date

	def is_valid(self, quiz) -> bool:
		return not self.is_used and not self.is_expired and self.quiz == quiz

	def save(self, *args, **kwargs):
		self.code = ''.join(
				(choice(string.ascii_letters + string.digits) for i in
				 range(16)))
		super(QuizCode, self).save(*args, **kwargs)
