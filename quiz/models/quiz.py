import json
from datetime import timedelta

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import FieldError, ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager

from .utils import is_answer_valid
from sorobrain.mixins.payment import PaidObjectMixin


class Quiz(PaidObjectMixin):
	"""
	A quiz object contains metadata about itself and a m2m field
	to the Question model. For all quizzes we assume that the
	ordering of the questions is unimportant, hence we can use an
	unordered m2m to Questions. Through a related_name attr we can
	also query the database for the quiz(zes) that a question may exist
	in.
	"""

	objects = models.Manager()

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

	title = models.CharField(max_length=256, verbose_name='Quiz Title')
	slug = models.SlugField(max_length=256, verbose_name='Slug', blank=True)
	description = RichTextUploadingField(config_name='minimal')
	level = models.CharField(max_length=128, verbose_name='French Level',
	                         choices=LEVEL_CHOICES)
	thumbnail = models.ImageField(upload_to='quiz/thumbnails/',
	                              # TODO: Add default thumbnail for quiz
	                              # default='quiz/thumbnails/no-thumbnail.png',
	                              null=True, blank=True)
	total_time = models.DurationField(verbose_name='Total Time',
	                                  default=timedelta(minutes=15))
	tags = TaggableManager()
	active = models.BooleanField(verbose_name='Active', default=True)
	created_on = models.DateTimeField(default=timezone.now,
	                                  verbose_name='Quiz Created On')

	def questions(self):
		return Question.objects.filter(quiz=self.id)

	# TODO: add get_absolute_url method for Quiz Model

	def save(self, *args, **kwargs):
		self.slug = slugify(self.title)
		super(Quiz, self).save(*args, **kwargs)

	def __str__(self):
		return self.title


class Question(models.Model):
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


	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = RichTextUploadingField()
	explanation = RichTextUploadingField()
	type = models.CharField(max_length=32, choices=QUESTION_TYPE_CHOICES)
	options = JSONField(blank=True, null=True)  # json array of option text
	answer = models.CharField(max_length=32, verbose_name="Answer: any of the following: T, F, 1, 2, 3, 4 or some text  ")
	created_on = models.DateTimeField(default=timezone.now)

	@property
	def is_answer_valid(self) -> bool:
		if self.type == 'text':
			return True
		answer_options = ('T', 'F', '1', '2', '3', '4')
		if self.answer in answer_options:
			return True
		else:
			return False

	@property
	def is_valid(self) -> bool:
		return self.is_answer_valid and (
				self.type != 'mcq' and self.options != '')

	def get_absolute_url(self):
		return reverse('quiz:question', args=[self.id])

	def save(self, *args, **kwargs):
		if not self.is_valid:
			raise FieldError("One of the entered fields is not valid")
		super(Question, self).save(*args, **kwargs)

	def __str__(self):
		return f'question_id: {self.id}'


class QuizQuestion(models.Model):
	"""This model is the intermediate class for the Quiz and Question model"""

	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	created_on = models.DateTimeField(default=timezone.now)


class QuizSubmission(models.Model):
	"""
	This model stores every attempt of a quiz for a user.
	The submission is the selected answers of the quiz. Its stored
	according to the ANSWER_CHOICES in the quiz model. That is,
	submission  is a json field that looks like the following:

	submission = {
		...
		<question_id>:<user_selection>
		...
	}

	The user_selection can only be one the ANSWER_CHOICES.
	"""

	class Meta:
		verbose_name = 'Quiz Submission'
		verbose_name_plural = 'Quiz Submissions'

	quiz = models.ForeignKey(Quiz, related_name='quiz_submission_quiz',
	                         on_delete=models.CASCADE)
	# TODO: Add competition ID here

	submission = JSONField()
	score = models.FloatField(null=True)
	start_time = models.DateTimeField()
	submit_time = models.DateTimeField()
	creation_time = models.DateTimeField(default=timezone.now)

	@property
	def attempt_time(self):
		return self.submit_time - self.start_time

	@property
	def took_too_long(self) -> bool:
		return self.quiz.total_time > self.attempt_time

	@property
	def is_submission_valid(self) -> bool:
		valid = True
		for question, answer in json.loads(self.submission).items():
			if not is_answer_valid(answer, Question.objects.get(id=question)):
				valid = False
				raise ValidationError(
					f"Answer format for {question}:{answer} is invalid")
		return valid

	@property
	def is_valid(self) -> bool:
		return self.is_submission_valid and not self.took_too_long

	# TODO: Finish this method for QuizSubmission
	def check_and_score(self):
		"""
		This method checks the QuizSubmission.submission against the
		correct answer for each question. Depending on the result of
		this is scores the test and saves the score to the database.
		"""
		pass
