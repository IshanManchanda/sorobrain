from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

from competition.models import CompetitionAccess, CompetitionCode
from competition.models.competition import CompetitionQuiz, Competition, CompetitionCertificate


class CompetitionQuizInline(admin.TabularInline):
	model = CompetitionQuiz
	fields = ('quiz',)
	extra = 1


class CompetitionAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'end_date')
	readonly_fields = ('slug', 'created_on', 'result', 'link')
	save_on_top = True
	radio_fields = {'level': admin.VERTICAL}
	save_as = True

	def link(self, obj):
		try:
			url = reverse('competition:send_certificate', args=[obj.slug])
		except NoReverseMatch:
			url = '/'
		return mark_safe(f"<a href='{url}'>Send Certificates</a>")
	link.allow_tags = True

	fieldsets = (
		(None, {
			'fields': ('title',
			           'slug',
			           'description',
			           'level',
			           'thumbnail',
			           'tags',)
		}),
		('Date', {
			'fields': ('start_date',
			           'end_date',
			           'created_on')
		}),
		('Pricing', {
			'fields': ('cost',
			           'discount',
			           'group_cost',)
		}),
		('Certificates', {
			'fields': ('link', )
		})
	)

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


class CompetitionCertificateAdmin(admin.ModelAdmin):
	list_display = ('user', 'competition')
	search_fields = ('user', 'competition')


admin.site.register(CompetitionCertificate, CompetitionCertificateAdmin)
