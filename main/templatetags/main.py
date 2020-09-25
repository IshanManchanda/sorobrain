import json

from django import template
from django.shortcuts import get_object_or_404

from competition.models import Competition

register = template.Library()


@register.filter
def addstr(arg1, arg2):
	"""concatenate arg1 & arg2"""
	return str(arg1) + str(arg2)


@register.simple_tag
def get_user_competition_rank(args):
	username, competition_id = args.split(',')
	c = get_object_or_404(Competition, id=competition_id)
	if not c.is_over:
		return "Not ended yet!"
	result = json.loads(c.result)
	try:
		rank = list(result.keys()).index(username) + 1  # rank is 1 indexed
	except:
		rank = '-'
	return rank


@register.simple_tag
def get_user_competition_score(args):
	username, competition_id = args.split(',')
	c = get_object_or_404(Competition, id=competition_id)
	if not c.is_over:
		return "Not ended yet!"
	result = json.loads(c.result)
	try:
		score = round(result[username], 4)
	except:
		score = '-'
	return score
