import secrets
from datetime import timedelta

from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


LEVEL_CHOICES = [
	(None, ''),
	('fluent', 'Fluent/Native Speaker'),
	('advanced', 'Advanced'),
	('intermediate', 'Intermediate'),
	('beginner', 'Beginner')
]


class Quiz(models.Model):
	class Meta:
		ordering = ['-created_on', ]
		verbose_name = 'Quiz'
		verbose_name_plural = 'Quizzes'

	id = models.CharField(max_length=128, primary_key=True,
	                      verbose_name='Quiz ID')
	title = models.CharField(max_length=256, verbose_name='Quiz Title')
	slug = models.SlugField(max_length=256, verbose_name='Slug', blank=True)
	description = RichTextUploadingField(config_name='minimal')
	level = models.CharField(max_length=128, verbose_name='French Level',
	                         choices=LEVEL_CHOICES)
	thumbnail = models.ImageField(upload_to='quiz/thumbnails/',
	                              # TODO: Add default thumbnail for quiz
	                              # default='quiz/thumbnails/no-thumbnail.png',
	                              null=True, blank=True)
	cost = models.IntegerField(verbose_name='Quiz Cost', default=0)
	total_time = models.DurationField(verbose_name='Total Time',
	                                  default=timedelta(minutes=15))
	tags = TaggableManager()
	active = models.BooleanField(verbose_name='Active')
	created_on = models.DateTimeField(default=timezone.now,
	                                  verbose_name='Quiz Created On')

	@staticmethod
	def generate_key(self):
		while True:
			key = secrets.token_urlsafe(16)  # Generates 64-character string
			if not self.__class__.objects.filter(id=key).exists():
				break
		return key

	def save(self, *args, **kwargs):
		self.id = self.generate_key(self)
		self.slug = slugify(self.title)
		super(Quiz, self).save(*args, **kwargs)
