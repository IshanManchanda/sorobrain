from django.contrib.postgres.forms import JSONField
from django.core.exceptions import ValidationError
from django.forms import fields, forms, ModelForm, Field

from quiz.models import Question
from sorobrain.utils.widgets import OptionsInputWidget


class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = (
			'question', 'explanation', 'answer', 'type', 'option1', 'option2',
			'option3', 'option4')
