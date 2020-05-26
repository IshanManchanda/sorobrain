import secrets

from django.db import models


class CustomIdMixin(models.Model):
	class Meta:
		abstract = True

	@staticmethod
	def generate_key(self):
		while True:
			key = secrets.token_urlsafe(16)  # Generates 64-character string
			if not self.__class__.objects.filter(id=key).exists():
				break
		return key
