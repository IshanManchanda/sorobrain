import string
import random
from datetime import timedelta

from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from taggit.managers import TaggableManager

from sorobrain.media_storages import PrivateMediaStorage
from sorobrain.mixins.common import CustomIdMixin
from sorobrain.mixins.payment import PaidObjectMixin
from main.models import User


class Session(models.Model):
	class Meta:
		verbose_name = 'Workshop Session'
		verbose_name_plural = 'Workshop Sessions'
		ordering = ('date',)

	title = models.CharField(max_length=128)
	description = models.TextField(max_length=1024)
	zoom_link = models.URLField(verbose_name='Link to Zoom Session')
	date = models.DateTimeField(verbose_name='Date of this Session')
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'session: {self.title} | id: {self.id}'


class Workshop(CustomIdMixin, PaidObjectMixin):
	class Meta:
		verbose_name = 'Workshop'
		verbose_name_plural = 'Workshops'
		ordering = ['-created_on']

	id = models.AutoField(primary_key=True, verbose_name="Workshop Id")
	title = models.CharField(max_length=128)
	thumbnail = models.ImageField(upload_to='workshops/thumbnails/',
	                              default='workshops/thumbnails/default_workshop.png',
	                              blank=True)
	slug = models.SlugField(blank=True)
	description = models.TextField(max_length=1024)
	video = models.CharField('Youtube Video ID', null=True, blank=True, max_length=64)
	sessions = models.ManyToManyField(Session,
	                                  related_name='workshop_sessions')
	date = models.DateTimeField()
	tags = TaggableManager(blank=True)
	include_book = models.BooleanField(default=False)
	active = models.BooleanField(default=False)
	related_file = models.FileField(upload_to='workshops/files/', storage=PrivateMediaStorage(),
	                                validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
	                                null=True, blank=True)
	created_on = models.DateTimeField(default=timezone.now)

	@classmethod
	def get_recent(cls):
		return cls.objects.filter(created_on__gte=(timezone.now() - timedelta(days=7)))

	@property
	def is_free(self):
		return self.sub_total < 1

	@property
	def is_expired(self):
		"""Returns true if the current time is after the workshop starts"""
		return timezone.now() > self.date

	@property
	def end_date(self):
		return self.sessions.order_by('date')[-1].date

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


class Code(models.Model):
	class Meta:
		verbose_name = 'Workshop Code'
		verbose_name_plural = 'Workshop Codes'
		ordering = ('-created_on',)

	code = models.CharField(max_length=256, unique=True)
	uses = models.IntegerField()
	expiry_date = models.DateTimeField()
	workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(default=timezone.now)

	@property
	def is_used(self) -> bool:
		return self.uses <= 0

	@property
	def is_expired(self) -> bool:
		"""Returns true if the current time is after the education time"""
		return timezone.now() > self.expiry_date

	def is_valid(self, workshop: Workshop) -> bool:
		return not self.is_used and not self.is_expired and self.workshop == workshop

	def use(self, *args, **kwargs):
		self.uses += -1
		super(Code, self).save(*args, **kwargs)

	def save(self, *args, **kwargs):
		self.code = ''.join(
				(random.choice(string.ascii_uppercase + string.digits) for i in
				 range(6)))
		super(Code, self).save(*args, **kwargs)


class WorkshopCertificate(models.Model):
	workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	certificate = models.ImageField(upload_to='workshops/certificates/')
