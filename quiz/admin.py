from django.contrib import admin
from django.contrib.postgres.fields import JSONField

from quiz.forms.question import QuestionForm
from quiz.models import Quiz, QuizAccess, QuizCode
from quiz.models.quiz import Question, QuizSubmission
from sorobrain.utils.widgets import OptionsInputWidget


class QuestionInline(admin.StackedInline):
	model = Question
	form = QuestionForm
	fieldsets = (
		(None, {
			'fields': ('type',
			           ('question', 'explanation'),
			           'answer',
			           ('option1', 'option2', 'option3', 'option4'),
			           ),
		}),
	)
	# formfield_overrides = {
	# 	JSONField: {'widget': OptionsInputWidget},
	# }
	save_as = True
	extra = 1
	can_delete = True


class QuizAdmin(admin.ModelAdmin):
	# form = UpdateQuizForm
	# add_form = AddQuizForm

	list_display = ('title', 'level', 'created_on')
	list_filter = ('level',)
	search_fields = ('title', 'tags', 'slug')
	ordering = ('title', '-created_on',)
	save_as = True
	save_on_top = True
	radio_fields = {'level': admin.VERTICAL}
	inlines = (QuestionInline,)

	fieldsets = (
		(None, {
			'fields': ('title',
			           ('description', 'level'),
			           'thumbnail', 'total_time')
		}),
		('Store', {
			'fields': (('cost', 'discount'),)
		}),
		('Categorization', {
			'fields': ('tags', 'active')
		})
	)

	# The following must be explicitly set to make sure django doesn't render it
	exclude = ('questions',)


admin.site.register(Quiz, QuizAdmin)


class QuestionAdmin(admin.ModelAdmin):
	list_display = ('id', 'type', 'question', 'answer', 'created_on')
	list_filter = ('type',)
	search_fields = ('question', 'explanation', 'answer')
	ordering = ('-created_on',)
	readonly_fields = ('id',)

	formfield_overrides = {
		JSONField: {'widget': OptionsInputWidget},
	}

	fieldsets = (
		(None, {
			'fields': ('type',
			           ('question', 'explanation'),
			           'answer',
			           ('option1', 'option2', 'option3', 'option4'))
		}),
	)


admin.site.register(Question, QuestionAdmin)


class QuizAccessAdmin(admin.ModelAdmin):
	list_display = ('user', 'quiz', 'created_on')
	list_filter = ('quiz', 'active')
	search_fields = ('user', 'quiz')
	readonly_fields = ('created_on',)


admin.site.register(QuizAccess, QuizAccessAdmin)


class QuizSubmissionAdmin(admin.ModelAdmin):
	list_display = ('user', 'quiz', 'competition', 'score', 'correct_answers', 'incorrect_answers', 'created_on')
	list_filter = ('quiz', 'competition')
	search_fields = ('user', 'quiz')
	readonly_fields = ('user', 'quiz', 'submission', 'score', 'correct_answers',
	                   'incorrect_answers', 'start_time', 'competition',
	                   'submit_time', 'created_on')


admin.site.register(QuizSubmission, QuizSubmissionAdmin)


class QuizCodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'uses', 'quiz', 'created_on')
	readonly_fields = ('code', 'created_on')


admin.site.register(QuizCode, QuizCodeAdmin)
