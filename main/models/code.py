import string
from random import choice

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from gfklookupwidget.fields import GfkLookupField


class DiscountCode(models.Model):
	class Meta:
		verbose_name = 'Discount Code'
		verbose_name_plural = 'Discount Codes'
		ordering = ('-created_on',)

	code = models.CharField(max_length=256, unique=True)
	uses = models.IntegerField()
	discount = models.IntegerField(verbose_name='Enter Discount Percentage',
	                               validators=[
		                               MaxValueValidator(99),
		                               MinValueValidator(1)])
	expiry_date = models.DateTimeField()
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE,
	                                 limit_choices_to={
		                                 "model__in": ("quiz", "workshop")})
	object_id = GfkLookupField('content_type')
	content_object = GenericForeignKey('content_type', 'object_id')
	created_on = models.DateTimeField(default=timezone.now)

	@property
	def is_used(self) -> bool:
		return self.uses <= 0

	@property
	def is_expired(self) -> bool:
		return timezone.now() > self.expiry_date

	def use(self, *args, **kwargs):
		self.uses += -1
		super(DiscountCode, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		self.code = ''.join(
				(choice(string.ascii_letters + string.digits) for i in
				 range(16)))
		super(DiscountCode, self).save(*args, **kwargs)
