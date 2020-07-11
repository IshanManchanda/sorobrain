from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
	PermissionsMixin
from django.db import models
from django.utils import timezone

from .mixins import UserData


class UserManager(BaseUserManager):
	def _create_user(self, username, email, name, phone, password, **extra):
		if not username:
			raise ValueError('Username must be set!')

		if not email:
			raise ValueError('Email ID must be set!')

		if not name:
			raise ValueError('Name must be set!')

		if not phone:
			raise ValueError('Phone number must be set!')

		if not password:
			raise ValueError('Password must be set!')

		email = self.normalize_email(email)
		user = self.model(
			username=username,
			email=email,
			name=name,
			phone=phone,
			**extra
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_user(self, username, email, name, phone, password, **extra):
		extra.setdefault('is_staff', False)
		extra.setdefault('is_superuser', False)
		return self._create_user(
			username, email, name, phone, password, **extra
		)

	def create_superuser(self, username, email, name, phone, password, **extra):
		extra['is_staff'] = True
		extra['is_superuser'] = True
		return self._create_user(
			username, email, name, phone, password, **extra
		)


class User(AbstractBaseUser, PermissionsMixin, UserData):
	username = models.CharField('Username', max_length=128, primary_key=True)
	# password field supplied by AbstractBaseUser
	# last_login field supplied by AbstractBaseUser

	# user data supplied by UserData mixin

	date_joined = models.DateTimeField('date joined', default=timezone.now)
	is_active = models.BooleanField(
		'active', default=True,
		help_text='Designates whether this user should be treated as active.',
	)
	is_staff = models.BooleanField(
		'staff status', default=False,
		help_text='Designates whether the user can log into this admin site.',
	)
	# is_superuser field provided by PermissionsMixin
	# groups field provided by PermissionsMixin
	# user_permissions field provided by PermissionsMixin

	objects = UserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email', 'name', 'phone', 'password']

	def get_full_name(self):
		return self.name

	@property
	def first_name(self):
		try:
			return self.name.split()[0]
		except IndexError:
			return ''

	@property
	def last_name(self):
		try:
			return self.name.split()[-1]
		except IndexError:
			return ''

	def __str__(self):
		return f'{self.username} <{self.email}>'
