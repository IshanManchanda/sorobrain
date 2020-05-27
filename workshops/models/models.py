from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from sorobrain.mixins.common import CustomIdMixin


class Workshop(CustomIdMixin):
	class Meta:
		verbose_name = 'Workshop'
		verbose_name_plural = 'Workshops'
		ordering = ['-created_on']

	id = models.AutoField(primary_key=True, verbose_name="Workshop Id")
	title = models.CharField(max_length=128)
	slug = models.SlugField(blank=True)
	description = models.TextField(max_length=1024)
	zoom_link = models.CharField(max_length=1024, blank=True)
	cost = models.IntegerField()
	discount = models.IntegerField(verbose_name='Discount Percentage',
	                               blank=True, null=True)
	date = models.DateTimeField()
	include_book = models.BooleanField(default=False)
	active = models.BooleanField(default=False)
	created_on = models.DateTimeField(default=timezone.now)

	def get_absolute_url(self):
		return reverse('workshops:workshop_store', args=[self.slug])

	def save(self, *args, **kwargs):
		self.slug = f"{slugify(self.title)}-{self.id}"
		super(Workshop, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.title} - {self.id}'
