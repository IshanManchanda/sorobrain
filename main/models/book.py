from django.db import models
from django.utils import timezone

from main.models import User


class BookAccess(models.Model):
	class Meta:
		verbose_name = 'Book Access'
		verbose_name_plural = 'Book Accesses'
		ordering = ('user', '-created_on')

	user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
	active = models.BooleanField(default=True)
	created_on = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return f'user: {self.user} has access to the book'
