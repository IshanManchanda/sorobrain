from django.shortcuts import get_object_or_404
from django.template import Library

from main.models import User

register = Library()


@register.simple_tag
def get_user_school(username):
	return get_object_or_404(User, username=username).school
