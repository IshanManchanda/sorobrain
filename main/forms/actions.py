from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from competition.models import Competition
from quiz.models import Quiz


class BulkQuickAccessForm(forms.Form):
	quizzes = forms.ModelMultipleChoiceField(queryset=Quiz.objects.all(),
	                                         widget=FilteredSelectMultiple("Quizzes", is_stacked=False))

class BulkCompetitionAccessForm(forms.Form):
	competitions = forms.ModelMultipleChoiceField(queryset=Competition.objects.all(),
	                                         widget=FilteredSelectMultiple("Competitions", is_stacked=False))
