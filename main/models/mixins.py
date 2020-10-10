from django.db import models
from django.utils import timezone

from phonenumber_field.modelfields import PhoneNumberField

from sorobrain.media_storages import PrivateMediaStorage


class UserData(models.Model):
	LEVEL_CHOICES = [
		('advanced', 'Advanced'),
		('intermediate', 'Intermediate'),
		('beginner', 'Beginner')
	]

	class Meta:
		abstract = True

	email = models.EmailField('Email Address', max_length=255)
	name = models.CharField('Full Name', max_length=128)
	phone = PhoneNumberField(null=True, blank=True)
	avatar = models.ImageField(storage=PrivateMediaStorage(),
	                           upload_to='user_data/avatars',
	                           null=True, blank=True)
	education = models.CharField('Education Level', max_length=265, null=True,
	                             blank=True)
	school = models.CharField('School', max_length=512, blank=True, null=True)
	city = models.CharField('City', max_length=512, blank=True, null=True)
	country = models.CharField('Country', max_length=512, blank=True, null=True)
	date_of_birth = models.DateField('Date of Birth', blank=True, null=True)
	gender = models.CharField('Gender', max_length=32, null=True, blank=True)
	level = models.CharField('French Level', max_length=128, null=True,
	                         blank=True, choices=LEVEL_CHOICES)
	# setting 5 levels of notifications <0 - 4>
	# 0 is disabled to 4 is all notifications
	notification_level = models.IntegerField('Notification Level', default='4')

	def profile_setup_progress(self):
		empty_fields = 0
		if self.gender is None:
			empty_fields += 1
		if self.phone is None:
			empty_fields += 1
		# ignoring user.avatar as it is not essential for profile setup
		if self.education is None:
			empty_fields += 1
		if self.level is None:
			empty_fields += 1

		return empty_fields


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
