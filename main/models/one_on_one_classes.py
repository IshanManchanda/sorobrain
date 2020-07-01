from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class OneOnOneClass(models.Model):
	LEVEL_CHOICES = [
		(None, ''),
		('fluent', 'Fluent/Native Speaker'),
		('advanced', 'Advanced'),
		('intermediate', 'Intermediate'),
		('beginner', 'Beginner')
	]

	class Meta:
		verbose_name = 'One on One Class'
		verbose_name_plural = 'One on One Classes'

	title = models.CharField(max_length=128)
	slug = models.CharField(max_length=256, unique=True)
	description = RichTextUploadingField()
	cost = models.IntegerField(help_text='Per class cost')
	duo_cost = models.IntegerField(help_text='The cost for two people taking a class together, per class')
	level = models.CharField(max_length=128, verbose_name='French Level',
	                         choices=LEVEL_CHOICES)
	active = models.BooleanField(verbose_name='Active', default=True)
	created_on = models.DateTimeField(default=timezone.now,
	                                  verbose_name='Created On')

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(OneOnOneClass, self).save(*args, **kwargs)

	def get_absolute_url(self):
		return reverse('class', args=[self.slug])
