from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from sorobrain.media_storages import PrivateMediaStorage


class UserData(models.Model):
	class Meta:
		abstract = True

	email = models.EmailField('Email Address', max_length=255)
	name = models.CharField('Full Name', max_length=128)
	phone = PhoneNumberField(null=True, blank=True)
	# TODO: Add storage=PrivateMediaStorage() below
	avatar = models.ImageField(upload_to='private/user_data/avatars', null=True,
	                           blank=True)
	education = models.CharField('Education Level', max_length=265, null=True,
	                             blank=True)
	gender = models.CharField('Gender', max_length=32, null=True, blank=True)
	level = models.CharField('French Level', max_length=128, null=True,
	                         blank=True)


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
