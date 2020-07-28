import string
from random import choice

from django.db import models
from django.utils import timezone

from main.models import User


class CompetitionAccess(models.Model):
	class Meta:
		verbose_name = 'Competition Access'
		verbose_name_plural = 'Competition Accesses'
		unique_together = ('user', 'competition')
		ordering = ('-created_on', 'competition')

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	competition = models.ForeignKey('competition.Competition', on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'user: {self.user} has access to {self.competition}'


class CompetitionCode(models.Model):
	class Meta:
		verbose_name = 'Competition Code'
		verbose_name_plural = 'Competition Codes'

	code = models.CharField(max_length=256, unique=True)
	uses = models.IntegerField()
	expiry_date = models.DateTimeField()
	competition = models.ForeignKey('competition.Competition', on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(default=timezone.now)

	@property
	def is_used(self) -> bool:
		return self.uses <= 0

	@property
	def is_expired(self) -> bool:
		"""Returns true if the current time is after the education time"""
		return timezone.now() > self.expiry_date

	def is_valid(self, competition) -> bool:
		return not self.is_used and not self.is_expired and self.competition == competition

	def use(self, *args, **kwargs):
		self.uses += -1
		super(CompetitionCode, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		self.code = ''.join(
				(choice(string.ascii_uppercase + string.digits) for i in
				 range(6)))
		super(CompetitionCode, self).save(*args, **kwargs)
