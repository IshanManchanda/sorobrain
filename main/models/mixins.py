from django.db import models
from django.utils import timezone


class UserData(models.Model):
	class Meta:
		abstract = True

	email = models.EmailField('Email Address', max_length=255)
	name = models.CharField('Full Name', max_length=128)
	phone = models.CharField('Phone Number', max_length=32)


class AttemptData(models.Model):
	class Meta:
		abstract = True

	attempt_id = models.AutoField('Attempt ID', primary_key=True)
	username = models.CharField('Username', max_length=64)

	timestamp = models.DateTimeField('Timestamp', default=timezone.now)
	successful = models.BooleanField('Successful', default=0)
	ip_address = models.GenericIPAddressField(
		'IP Address', null=True, blank=True
	)

	def __str__(self):
		return f'{self.username} @ {self.timestamp}'
