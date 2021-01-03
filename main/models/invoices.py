from django.db import models
from django.utils import timezone


class Invoice(models.Model):
	class Meta:
		verbose_name = "Invoice"
		verbose_name_plural = "Invoices"

	user = models.ForeignKey('main.User', on_delete=models.CASCADE)
	description = models.CharField(max_length=512)
	amount = models.IntegerField()
	paid = models.BooleanField(default=True)
	date = models.DateTimeField(default=timezone.now)
	invoice_html = models.TextField(null=True)

	def __str__(self):
		return f"Invoice no. {self.id} - {self.user.username}"
