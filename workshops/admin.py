from django.contrib import admin

from workshops.models import Workshop, WorkshopAccess, Session, Code


class WorkshopAdmin(admin.ModelAdmin):
	list_display = ('title', 'date', 'cost', 'discount', 'created_on')
	list_filter = ('active', 'include_book',)
	search_fields = ('title', 'description', 'zoom_link')
	readonly_fields = ('slug',)


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


admin.site.register(Code, CodeAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Workshop, WorkshopAdmin)
admin.site.register(WorkshopAccess, WorkshopAccessAdmin)
