from django.contrib import admin

from competition.models import CompetitionAccess, CompetitionCode
from competition.models.competition import CompetitionQuiz, Competition


class CompetitionQuizInline(admin.TabularInline):
	model = CompetitionQuiz
	fields = ('quiz',)
	extra = 1


class CompetitionAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'end_date')
	readonly_fields = ('slug', 'created_on', 'result')
	inlines = (CompetitionQuizInline,)


admin.site.register(Competition, CompetitionAdmin)


class CompetitionAccessAdmin(admin.ModelAdmin):
	list_display = ('user', 'competition', 'created_on')
	search_fields = ('user', 'competition')
	list_filter = ('active',)


admin.site.register(CompetitionAccess, CompetitionAccessAdmin)


class CompetitionCodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'uses', 'competition', 'created_on')
	readonly_fields = ('code', 'created_on')


admin.site.register(CompetitionCode, CompetitionCodeAdmin)
