from django.contrib import admin
from quiz.models import Quiz
from quiz.models.quiz import Question


class QuizAdmin(admin.ModelAdmin):
	# form = UpdateQuizForm
	# add_form = AddQuizForm

	list_display = ('title', 'level', 'created_on')
	list_filter = ('level',)
	search_fields = ('title', 'tags', 'slug')
	ordering = ('title', '-created_on',)

	fieldsets = (
		(None, {
			'fields': ('title', 'description', 'level', 'cost', 'thumbnail',
			           'total_time', 'tags', 'active')
		}),
	)


admin.site.register(Quiz, QuizAdmin)


class QuestionAdmin(admin.ModelAdmin):
	list_display = ('id', 'type', 'question', 'answer', 'created_on')
	list_filter = ('type',)
	search_fields = ('question', 'explanation', 'answer')
	ordering = ('-created_on',)
	# REVIEW: Check the fields that need to be made readonly
	readonly_fields = ('id',)


admin.site.register(Question, QuestionAdmin)

