import datetime

from django.db import models
from django.utils import timezone

from .mixins import AttemptData, UserData


class User(UserData):
	class Meta:
		verbose_name = 'User'
		verbose_name_plural = 'Users'

	username = models.CharField(
		max_length=64,
		primary_key=True,
		verbose_name='Username'
	)

	user_key = models.CharField(
		max_length=128,
		default='',
		verbose_name='User Key'
	)
	timestamp = models.DateTimeField(
		default=timezone.now,
		verbose_name='Confirmation / Reset Request Generation Time'
	)
	confirmed = models.BooleanField(default=0, verbose_name='Confirmed')

	def __str__(self):
		return f'{self.username} <{self.email}>'

	def confirm(self):
		if self.is_action_valid():
			self.confirmed = 1
			self.save()
			return True
		return False

	def is_action_valid(self):
		return self.timestamp >= timezone.now() - datetime.timedelta(days=1)


class LoginAttempt(AttemptData):
	class Meta:
		verbose_name = 'Login Attempt'
		verbose_name_plural = 'Login Attempts'


class RegisterAttempt(AttemptData, UserData):
	class Meta:
		verbose_name = 'Register Attempt'
		verbose_name_plural = 'Register Attempts'
