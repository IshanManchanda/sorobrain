from django.db import models
from django.utils import timezone


class Ledger(models.Model):
	"""
	This class keeps a record of all transactions done using Soromoney.

	Points of Transaction using Soromoney:
		1. Buy Quiz        [*]
		2. Buy Workshop    [*]
		3. Referee Credit  [*]
		4. Referrer Credit [*]
	"""
	class Meta:
		verbose_name = 'Ledger'
		verbose_name_plural = 'Ledgers'

	user = models.ForeignKey('main.User', on_delete=models.CASCADE)
	debit = models.IntegerField(null=True, blank=True)
	credit = models.IntegerField(null=True, blank=True)
	description = models.CharField(max_length=512, null=True, blank=True)
	time = models.DateTimeField(default=timezone.now)

	def __str__(self):
		if self.debit is None:
			return f"{self.description} debited {self.debit}"
		return f"{self.description} credited {self.credit}"
