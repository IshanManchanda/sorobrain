from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.safestring import mark_safe

from workshops.models import Workshop, WorkshopAccess, Session, Code
from workshops.models.models import WorkshopCertificate


class SessionInline(admin.StackedInline):
	model = Workshop.sessions.through
	extra = 1


class WorkshopAdmin(admin.ModelAdmin):
	def link(self, obj):
		try:
			url = reverse('workshops:send_certificate', args=[obj.slug])
		except NoReverseMatch:
			url = '/'
		return mark_safe(f"<a href='{url}'>Send Certificates</a>")
	link.allow_tags = True

	list_display = ('title', 'date', 'cost', 'discount', 'created_on')
	list_filter = ('active', 'include_book',)
	search_fields = ('title', 'description', 'zoom_link')
	readonly_fields = ('link',)
	exclude = ('sessions',)
	inlines = (SessionInline,)
	save_as_new = True


class WorkshopAccessAdmin(admin.ModelAdmin):
	list_display = ('user', 'workshop', 'created_on')
	list_filter = ('workshop', 'active')
	search_fields = ('user', 'workshop')
	readonly_fields = ('created_on',)


class SessionAdmin(admin.ModelAdmin):
	list_display = ('title', 'created_on', 'zoom_link')
	search_fields = ('title',)
	readonly_fields = ('created_on',)


class CodeAdmin(admin.ModelAdmin):
	list_display = ('code', 'uses', 'workshop', 'expiry_date')
	search_fields = ('workshop',)
	list_filter = ('workshop',)
	readonly_fields = ('created_on', 'code')


class WorkshopCertificateAdmin(admin.ModelAdmin):
	list_display = ('user', 'workshop')
	list_filter = ('workshop',)
	search_fields = ('user', 'workshop')


admin.site.register(Code, CodeAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(WorkshopAccess, WorkshopAccessAdmin)
admin.site.register(WorkshopCertificate, WorkshopCertificateAdmin)
