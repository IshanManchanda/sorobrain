from django.contrib import admin
from quiz.models import Quiz
from quiz.models.quiz import Question


class QuestionInline(admin.StackedInline):
	model = Question
	fieldsets = (
		(None, {
			'fields': ('type',
			           ('question', 'explanation'),
			           ('answer', 'options')
			           ),
		}),
	)
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
	# REVIEW: Check the fields that need to be made readonly
	readonly_fields = ('id',)

	fieldsets = (
		(None, {
			'fields': ('type',
			           ('question', 'explanation'),
			           'answer',
			           'options')
		}),
	)


admin.site.register(Question, QuestionAdmin)
