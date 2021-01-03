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

from main.models import User
from .utils import is_answer_valid, evaluate_mcq, evaluate_bool, evaluate_text
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
		('beginner', 'Beginner'),
		('any', 'French Learner of any Level')
	]

	class Meta:
		ordering = ['-created_on', ]
		verbose_name = 'Quiz'
		verbose_name_plural = 'Quizzes'

	title = models.CharField(max_length=256, verbose_name='Quiz Title')
	slug = models.SlugField(max_length=256, verbose_name='Slug', blank=True,
	                        unique_for_date=True)
	description = RichTextUploadingField(config_name='minimal')
	level = models.CharField(max_length=128, verbose_name='French Level',
	                         choices=LEVEL_CHOICES)
	thumbnail = models.ImageField(upload_to='quiz/thumbnails/',
	                              null=True, blank=True,
	                              default='quiz/thumbnails/quiz-placeholder.jpg')
	total_time = models.DurationField(verbose_name='Total Time',
	                                  default=timedelta(minutes=15))
	tags = TaggableManager()
	active = models.BooleanField(verbose_name='Active', default=True)
	not_for_sale = models.BooleanField(verbose_name='Not For Sale', default=False)
	created_on = models.DateTimeField(default=timezone.now,
	                                  verbose_name='Quiz Created On')

	@property
	def questions(self):
		return Question.objects.filter(quiz=self.id)

	@property
	def question_id_list(self):
		return [question.id for question in self.questions]

	@classmethod
	def get_recent(cls):
		return cls.objects.filter(created_on__gte=(timezone.now() - timedelta(days=7)))

	def get_start_url(self):
		return reverse('quiz:start', args=[self.slug])

	def get_attempt_url(self, quiz_submission):
		return reverse('quiz:attempt', args=[self.slug, quiz_submission.id])

	def get_checked_url(self, quiz_submission):
		return reverse('quiz:checked', args=[self.slug, quiz_submission.id])

	def get_absolute_url(self):
		return reverse('quiz:buy', args=[self.slug])

	def save(self, *args, **kwargs):
		self.slug = slugify(f"{self.title}-{self.id}")
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
		ordering = ['created_on']

	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	question = RichTextUploadingField()
	explanation = RichTextUploadingField()
	type = models.CharField(max_length=32, choices=QUESTION_TYPE_CHOICES)
	option1 = models.CharField(max_length=512, null=True, blank=True)
	option2 = models.CharField(max_length=512, null=True, blank=True)
	option3 = models.CharField(max_length=512, null=True, blank=True)
	option4 = models.CharField(max_length=512, null=True, blank=True)
	answer = models.CharField(max_length=1024,
	                          verbose_name="Answer",
	                          help_text="any of the following: T, F, 1, 2, 3, 4 or some text. "
	                                    "For text answers separate multiple correct choices with '|' (pipe) character.")
	created_on = models.DateTimeField(default=timezone.now)

	@property
	def options(self):
		return [self.option1, self.option2, self.option3, self.option4]

	def is_answer_valid(self) -> bool:
		if self.type == 'text':
			return True
		answer_options = ('T', 'F', '1', '2', '3', '4')
		if self.answer in answer_options:
			return True
		else:
			return False

	def is_options_valid(self):
		if self.type == 'mcq':
			return any(self.options)
		else:
			return not any(self.options)

	@property
	def is_valid(self) -> bool:
		return self.is_answer_valid() and (self.is_options_valid())

	def get_absolute_url(self):
		return reverse('quiz:question', args=[self.id])

	def clean(self):
		if not self.is_answer_valid():
			raise ValidationError(
					f'Answer must any of the following: T, F, 1, 2, 3, 4 or some text, not {self.answer}')
		if not self.is_options_valid():
			raise ValidationError(
					f'Options must be set only for mcq type! not for {self.type} type')

	def save(self, *args, **kwargs):
		super(Question, self).save(*args, **kwargs)

	def __str__(self):
		return f'question_id: {self.id}'


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
		unique_together = ('user', 'quiz', 'competition')

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	quiz = models.ForeignKey(Quiz, related_name='quiz_submission_quiz',
	                         on_delete=models.CASCADE)
	competition = models.ForeignKey('competition.Competition',
	                                on_delete=models.CASCADE,
	                                null=True)
	submission = JSONField(null=True, default=dict)
	score = models.FloatField(null=True)
	correct_answers = models.IntegerField(null=True)
	incorrect_answers = models.IntegerField(null=True)
	start_time = models.DateTimeField()
	submit_time = models.DateTimeField(null=True)
	created_on = models.DateTimeField(default=timezone.now)

	@property
	def expiry_time(self):
		return self.start_time + self.quiz.total_time

	@property
	def attempt_time(self):
		return self.submit_time - self.start_time

	@property
	def attempt_time_human(self):
		return int((self.submit_time - self.start_time).seconds / 60)

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

	def get_result(self):
		submission = [(Question.objects.get(id=int(q_id)), sa) for q_id, sa in
		              json.loads(self.submission).items()]
		result = []
		for question, selected_answer in submission:
			if question.type == 'mcq':
				result.append(
						(question, selected_answer, evaluate_mcq(question,
						                                         selected_answer)))
			if question.type == 'bool':
				result.append(
						(question, selected_answer, evaluate_bool(question,
						                                          selected_answer)))
			if question.type == 'text':
				result.append(
						(question, selected_answer, evaluate_text(question,
						                                          selected_answer)))

		return result

	def check_and_score(self):
		"""
		This method checks the QuizSubmission.submission against the
		correct answer for each question. Depending on the result of
		this is scores the test and saves the score to the database.
		returns: result array of the form
		result = [(question_id, right_or_wrong)]
		"""

		result = self.get_result()

		correct_answers_number = 0
		incorrect_answers_number = 0

		for question_id, selected_answer, evaluation in result:
			if evaluation is True:
				correct_answers_number += 1
			elif evaluation == -1:
				incorrect_answers_number += 1
			else:
				incorrect_answers_number += 1

		self.correct_answers = correct_answers_number
		self.incorrect_answers = incorrect_answers_number
		if self.attempt_time > self.quiz.total_time:
			remaining_time = 0
			self.score = 0
		else:
			remaining_time = self.quiz.total_time - self.attempt_time
			self.score = ((correct_answers_number / (correct_answers_number + incorrect_answers_number) * 100) * (
					((abs(remaining_time.total_seconds()) / abs(self.quiz.total_time.total_seconds())) * 100) / 10))
		self.save()

		return result
