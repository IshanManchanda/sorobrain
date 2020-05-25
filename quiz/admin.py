from django.contrib import admin
from quiz.models import Quiz


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
