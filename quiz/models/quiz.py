import secrets
from datetime import timedelta

from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

from sorobrain.mixins.common import CustomIdMixin


class Quiz(models.Model):
	"""
	A quiz object contains metadata about itself and a m2m field
	to the Question model. For all quizzes we assume that the
	ordering of the questions is unimportant, hence we can use an
	unordered m2m to Questions. Through a related_name attr we can
	also query the database for the quiz(zes) that a question may exist
	in.
	"""
	
	LEVEL_CHOICES = [
		(None, ''),
		('fluent', 'Fluent/Native Speaker'),
		('advanced', 'Advanced'),
		('intermediate', 'Intermediate'),
		('beginner', 'Beginner')
	]

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


class Question(CustomIdMixin):
	"""
	Question objects store the question and the answers to that question
	There are three types of questions:
		1. MCQs: The options are stored in question.options as a json
		and the correct answer is the index value of the option starting
		from 1.
		2. True or False: The answer is stored as 'T' of 'F'.
		3. Text: The answer is stored as some string.

	answer_options = [
		('T', 'True'),
		('F', 'False),
		('1', 'One'),
		('2', 'Two'),
		('3', 'Three'),
		('4', 'Four'),
		('<str>', '<str>') # This is why we cannot enforce these options
	]
	"""

	QUESTION_TYPE_CHOICES = [
		('mcq', 'Multiple Choice Question'),
		('bool', 'True or False'),
		('text', 'Text Answer')
	]

	class Meta:
		verbose_name = 'Question'
		verbose_name_plural = 'Questions'
		ordering = ['-created_on']

	id = models.CharField(max_length=128, primary_key=True,
	                      verbose_name='Quiz ID')
	question = RichTextUploadingField()
	explanation = RichTextUploadingField()
	type = models.CharField(max_length=32, choices=QUESTION_TYPE_CHOICES)
	options = models.CharField(max_length=1024, blank=True,
	                           null=True)  # json array of option text
	answer = models.CharField(max_length=32)
	created_on = models.DateTimeField(default=timezone.now)

	def get_absolute_url(self):
		return reverse('quiz:question', args=[self.id])

	def save(self, *args, **kwargs):
		self.id = self.generate_key(self)  # provided by CustomIdMixin
		super(Question, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.question} | id:{self.id}'
