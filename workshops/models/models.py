from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from sorobrain.mixins.common import CustomIdMixin
from sorobrain.mixins.payment import PaidObjectMixin
from main.models import User


class Workshop(CustomIdMixin, PaidObjectMixin):
	class Meta:
		verbose_name = 'Workshop'
		verbose_name_plural = 'Workshops'
		ordering = ['-created_on']

	id = models.AutoField(primary_key=True, verbose_name="Workshop Id")
	title = models.CharField(max_length=128)
	slug = models.SlugField(blank=True)
	description = models.TextField(max_length=1024)
	zoom_link = models.CharField(max_length=1024, blank=True)
	date = models.DateTimeField()
	tags = TaggableManager()
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


class WorkshopAccess(models.Model):
	class Meta:
		verbose_name = 'Workshop Access'
		verbose_name_plural = 'Workshop Accesses'
		unique_together = ('user', 'workshop')
		ordering = ('workshop', '-created_on')

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'user: {self.user} has access to {self.workshop}'
